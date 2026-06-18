from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.discovery import ArticleMetadata

from .classification import ClassificationOutput
from .critic_output import CriticOutput
from .super_summary import SuperSummary
from .synthesis import SynthesisOutput


class ProcessingStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PDF_EXTRACTION_FAILED = "PDF_EXTRACTION_FAILED"
    READER_FAILED = "READER_FAILED"
    CLASSIFIER_FAILED = "CLASSIFIER_FAILED"
    CRITIC_FAILED = "CRITIC_FAILED"
    CITATION_FAILED = "CITATION_FAILED"


@dataclass
class ArticleResult:
    metadata: ArticleMetadata
    processing_status: ProcessingStatus
    super_summary: SuperSummary | None
    classification: ClassificationOutput | None
    critic_output: CriticOutput | None
    citation_count: int | None
    ifrd: float | None
    error: str | None = None
    citation_source: str | None = None


@dataclass
class PipelineResult:
    article_results: list[ArticleResult]
    synthesis: SynthesisOutput | None
