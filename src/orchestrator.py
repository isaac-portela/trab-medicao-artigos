from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from src.agents import classifier_agent, critic_agent, reader_agent, synthesizer_agent
from src.agents._factory import get_agent_attr
from src.config import BASE_RETRY_DELAY, CHECKPOINTS_DIR, DEFAULT_DELAY, MAX_RETRIES
from src.discovery import ArticleMetadata
from src.ifrd import calculate_ifrd
from src.models import (
    ArticleMetadataDTO,
    ArticleResult,
    ArticleResultSummary,
    ClassifierInput,
    ClassificationOutput,
    CriticInput,
    CriticOutput,
    PipelineResult,
    ProcessingStatus,
    ReaderInput,
    SuperSummary,
    SynthesizerInput,
    SynthesisOutput,
)
from src.services import CitationLookupService, extract_pdf_text
from src.runtime import CheckpointStore


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ArticleLogContext:
    index: int | None
    total: int | None
    key: str
    title: str

    @property
    def prefix(self) -> str:
        position = f"{self.index}/{self.total} " if self.index is not None and self.total is not None else ""
        return f"[article {position}{self.key}] {self.title}"


class GeminiStructuredExecutor:
    def __init__(self, api_key: str | None = None):
        from google import genai
        from google.genai import types

        self._types = types
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()

    async def run(self, agent: Any, payload: BaseModel, output_schema: type[BaseModel]) -> BaseModel:
        return await asyncio.to_thread(self._run_sync, agent, payload, output_schema)

    def _run_sync(self, agent: Any, payload: BaseModel, output_schema: type[BaseModel]) -> BaseModel:
        instruction = get_agent_attr(agent, "instruction")
        prompt = (
            f"{instruction}\n\n"
            "Entrada JSON validada para esta etapa:\n"
            f"{payload.model_dump_json(indent=2)}"
        )
        response = self.client.models.generate_content(
            model=get_agent_attr(agent, "model"),
            contents=prompt,
            config=self._types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=output_schema,
                temperature=0.1,
            ),
        )
        if not response.text:
            raise ValueError("empty Gemini response")
        return output_schema.model_validate_json(response.text)


class PipelineOrchestrator:
    def __init__(
        self,
        delay_seconds: float = DEFAULT_DELAY,
        max_retries: int = MAX_RETRIES,
        base_retry_delay: float = BASE_RETRY_DELAY,
        executor: GeminiStructuredExecutor | None = None,
        citation_service: CitationLookupService | None = None,
        checkpoint_store: CheckpointStore | None = None,
    ):
        if delay_seconds < 0:
            raise ValueError("delay_seconds must be >= 0")
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay
        self.executor = executor or GeminiStructuredExecutor()
        self.citation_service = citation_service or CitationLookupService()
        self.checkpoint_store = checkpoint_store or CheckpointStore(CHECKPOINTS_DIR)
        self.article_sequence = self._build_article_sequence()

    @staticmethod
    def _build_article_sequence() -> Any | None:
        try:
            from google.adk.agents import SequentialAgent

            return SequentialAgent(
                name="article_classification_sequence",
                sub_agents=[reader_agent, classifier_agent, critic_agent],
            )
        except Exception:
            return None

    @staticmethod
    def _metadata_dto(metadata: ArticleMetadata) -> ArticleMetadataDTO:
        return ArticleMetadataDTO(
            folder_path=str(metadata.folder_path),
            title=metadata.title,
            student=metadata.student,
            group=metadata.group,
            link=metadata.link,
        )

    async def _run_with_retries(
        self,
        agent: Any,
        payload: BaseModel,
        output_schema: type[BaseModel],
        article_title: str,
        agent_name: str,
    ) -> BaseModel:
        delay = self.base_retry_delay
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                result = await self.executor.run(agent, payload, output_schema)
                if self.delay_seconds > 0:
                    await asyncio.sleep(self.delay_seconds)
                return result
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "%s failed for %s on attempt %s/%s: %s",
                    agent_name,
                    article_title,
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2
        raise RuntimeError(f"{agent_name} failed for {article_title}: {last_error}") from last_error

    async def process_article(self, metadata: ArticleMetadata, context: ArticleLogContext | None = None) -> ArticleResult:
        context = context or ArticleLogContext(None, None, self.checkpoint_store.article_key(metadata), metadata.title)
        logger.info("%s: starting", context.prefix)
        extraction = extract_pdf_text(metadata.pdf_path)
        status = ProcessingStatus.SUCCESS
        extraction_error = None
        if not extraction.success:
            status = ProcessingStatus.PDF_EXTRACTION_FAILED
            extraction_error = extraction.error_message
            logger.warning("%s: PDF extraction failed: %s", context.prefix, extraction.error_message)
        else:
            logger.info("%s: extracted %s PDF characters", context.prefix, len(extraction.text))

        metadata_dto = self._metadata_dto(metadata)
        try:
            reader_input = ReaderInput(
                metadata=metadata_dto,
                extracted_text=extraction.text,
                pdf_extraction_failed=not extraction.success,
            )
            super_summary = await self._run_with_retries(
                reader_agent,
                reader_input,
                SuperSummary,
                metadata.title,
                "Reader_Agent",
            )
        except Exception as exc:
            logger.error("%s: Reader failed: %s", context.prefix, exc)
            result = self._result(
                metadata,
                ProcessingStatus.READER_FAILED,
                citation_count=self._safe_citation(metadata.title).count,
                error=str(exc),
            )
            self.checkpoint_store.save(result)
            return result
        logger.info("%s: Reader completed", context.prefix)

        try:
            classifier_input = ClassifierInput(metadata=metadata_dto, super_summary=super_summary)
            classification = await self._run_with_retries(
                classifier_agent,
                classifier_input,
                ClassificationOutput,
                metadata.title,
                "Classifier_Agent",
            )
        except Exception as exc:
            logger.error("%s: Classifier failed: %s", context.prefix, exc)
            result = self._result(
                metadata,
                ProcessingStatus.CLASSIFIER_FAILED,
                super_summary=super_summary,
                citation_count=self._safe_citation(metadata.title).count,
                error=str(exc),
            )
            self.checkpoint_store.save(result)
            return result
        logger.info("%s: Classifier completed", context.prefix)

        try:
            critic_input = CriticInput(
                metadata=metadata_dto,
                super_summary=super_summary,
                classification=classification,
            )
            critic_output = await self._run_with_retries(
                critic_agent,
                critic_input,
                CriticOutput,
                metadata.title,
                "Critic_Agent",
            )
        except Exception as exc:
            logger.error("%s: Critic failed: %s", context.prefix, exc)
            result = self._result(
                metadata,
                ProcessingStatus.CRITIC_FAILED,
                super_summary=super_summary,
                classification=classification,
                citation_count=self._safe_citation(metadata.title).count,
                error=str(exc),
            )
            self.checkpoint_store.save(result)
            return result
        logger.info("%s: Critic completed", context.prefix)

        citation = self._safe_citation(metadata.title)
        if citation.count is None and status == ProcessingStatus.SUCCESS:
            status = ProcessingStatus.CITATION_FAILED
        ifrd = calculate_ifrd(critic_output.rubric_scores())
        result = self._result(
            metadata,
            status,
            super_summary=super_summary,
            classification=classification,
            critic_output=critic_output,
            citation_count=citation.count,
            ifrd=ifrd,
            error=extraction_error if status == ProcessingStatus.PDF_EXTRACTION_FAILED else citation.error_message,
        )
        self.checkpoint_store.save(result)
        logger.info("%s: completed with status=%s ifrd=%s", context.prefix, result.processing_status.value, result.ifrd)
        return result

    def _safe_citation(self, title: str):
        try:
            return self.citation_service.get_citation_count(title)
        except Exception as exc:
            logger.warning("Citation lookup failed for %s: %s", title, exc)
            from src.services.citation_lookup import CitationResult

            return CitationResult(count=None, source="N/A", error_message=str(exc))

    @staticmethod
    def _result(
        metadata: ArticleMetadata,
        processing_status: ProcessingStatus,
        super_summary: SuperSummary | None = None,
        classification: ClassificationOutput | None = None,
        critic_output: CriticOutput | None = None,
        citation_count: int | None = None,
        ifrd: float | None = None,
        error: str | None = None,
    ) -> ArticleResult:
        return ArticleResult(
            metadata=metadata,
            processing_status=processing_status,
            super_summary=super_summary,
            classification=classification,
            critic_output=critic_output,
            citation_count=citation_count,
            ifrd=ifrd,
            error=error,
        )

    @staticmethod
    def _summary_for_synthesis(result: ArticleResult) -> ArticleResultSummary:
        return ArticleResultSummary(
            folder_name=result.metadata.folder_path.name,
            title=result.metadata.title,
            theme=result.classification.theme if result.classification else None,
            syllabus_units=result.classification.syllabus_units if result.classification else [],
            syllabus_topics=result.classification.syllabus_topics if result.classification else [],
            super_summary=result.super_summary,
            rubric_scores=result.critic_output.rubric_scores() if result.critic_output else None,
        )

    async def run_synthesis(self, results: list[ArticleResult]) -> SynthesisOutput | None:
        payload = SynthesizerInput(articles=[self._summary_for_synthesis(result) for result in results])
        try:
            return await self._run_with_retries(
                synthesizer_agent,
                payload,
                SynthesisOutput,
                "corpus",
                "Synthesizer_Agent",
            )
        except Exception as exc:
            logger.error("Synthesis failed: %s", exc)
            return None

    async def run(
        self,
        articles: list[ArticleMetadata],
        progress_callback: Callable[[int, int, str], None] | None = None,
        resume: bool = False,
        only_missing: bool = False,
    ) -> PipelineResult:
        results: list[ArticleResult] = []
        total = len(articles)
        for index, article in enumerate(articles, start=1):
            context = ArticleLogContext(index, total, self.checkpoint_store.article_key(article), article.title)
            if resume or only_missing:
                checkpoint = self.checkpoint_store.load(article)
                if checkpoint is not None:
                    logger.info("%s: loaded from checkpoint", context.prefix)
                    results.append(checkpoint)
                    if progress_callback:
                        progress_callback(index, total, article.title)
                    continue
            result = await self.process_article(article, context=context)
            results.append(result)
            if progress_callback:
                progress_callback(index, total, article.title)
        synthesis = await self.run_synthesis(results) if results else None
        return PipelineResult(article_results=results, synthesis=synthesis)
