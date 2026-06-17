from __future__ import annotations

from pathlib import Path

from src.agents.prompt_loader import load_prompt
from src.discovery import ArticleMetadata
from src.models import ArticleResult, ClassificationOutput, ProcessingStatus, SuperSummary
from src.runtime import CheckpointStore


def test_prompts_are_versioned_and_non_empty():
    for prompt_name in ["reader.md", "classifier.md", "critic.md", "synthesizer.md"]:
        prompt = load_prompt(prompt_name)
        assert len(prompt) > 80


def test_checkpoint_round_trip_preserves_intermediate_outputs(tmp_path):
    metadata = ArticleMetadata(
        folder_path=Path("artigos") / "01 - Example",
        title="Example Article",
        student="Ana",
        group="Turma",
        link="https://example.test",
        pdf_path=Path("artigos") / "01 - Example" / "artigo.pdf",
    )
    summary = SuperSummary(
        core_research_question="Qual é a pergunta?",
        methodology_description="Estudo empírico controlado.",
        key_findings=["Achado principal"],
        statistical_techniques=["Teste t"],
    )
    classification = ClassificationOutput(
        theme="Métricas",
        publication_year=2020,
        publisher_entity="ACM",
        venue_type="Revista (Journal)",
        study_type="Experimento Controlado",
        research_nature="Prática (Empírica)",
        data_nature="Quantitativa",
        sample_size="20 participantes",
        statistical_methods=["Teste t"],
        software_metrics=["LOC"],
        syllabus_units=["Unidade 1"],
        syllabus_topics=["Métricas de produto"],
    )
    result = ArticleResult(
        metadata=metadata,
        processing_status=ProcessingStatus.CRITIC_FAILED,
        super_summary=summary,
        classification=classification,
        critic_output=None,
        citation_count=3,
        ifrd=None,
        error="critic failed",
    )

    store = CheckpointStore(tmp_path)
    path = store.save(result)
    loaded = store.load(metadata)

    assert path.is_file()
    assert loaded is not None
    assert loaded.processing_status == ProcessingStatus.CRITIC_FAILED
    assert loaded.super_summary == summary
    assert loaded.classification == classification
    assert loaded.citation_count == 3
    assert loaded.error == "critic failed"
