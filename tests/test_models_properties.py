from __future__ import annotations

from datetime import datetime

import pytest
from hypothesis import given, settings, strategies as st
from pydantic import ValidationError

from src.config import TOPICOS_EMENTA
from src.models import ClassificationOutput, CriticOutput, RubricScore, SuperSummary


@settings(max_examples=100)
@given(
    question=st.text(min_size=1).filter(lambda value: bool(value.strip())),
    methodology=st.text(min_size=1).filter(lambda value: bool(value.strip())),
    findings=st.lists(st.text(min_size=1).filter(lambda value: bool(value.strip())), min_size=1, max_size=10),
    techniques=st.lists(st.text(min_size=1).filter(lambda value: bool(value.strip())), max_size=5),
)
def test_property_5_super_summary_accepts_valid_shape(question, methodology, findings, techniques):
    summary = SuperSummary(
        core_research_question=question,
        methodology_description=methodology,
        key_findings=findings,
        statistical_techniques=techniques,
    )
    assert summary.key_findings


@given(findings=st.lists(st.text(min_size=1), min_size=0, max_size=15))
def test_property_5_super_summary_rejects_invalid_findings_count(findings):
    if 1 <= len(findings) <= 10:
        return
    with pytest.raises(ValidationError):
        SuperSummary(
            core_research_question="Pergunta válida",
            methodology_description="Método válido",
            key_findings=findings,
            statistical_techniques=[],
        )


def _valid_classification(**overrides):
    data = {
        "theme": "Métricas de software",
        "publication_year": 2020,
        "publisher_entity": "ACM",
        "venue_type": "Revista (Journal)",
        "study_type": "Estudo de Caso",
        "research_nature": "Prática (Empírica)",
        "data_nature": "Quantitativa",
        "sample_size": "10 projetos",
        "statistical_methods": ["Estatística descritiva"],
        "software_metrics": ["LOC"],
        "syllabus_units": ["Unidade 1"],
        "syllabus_topics": [TOPICOS_EMENTA[0]],
    }
    data.update(overrides)
    return ClassificationOutput(**data)


@settings(max_examples=100)
@given(year=st.one_of(st.none(), st.integers(min_value=1900, max_value=datetime.now().year)))
def test_property_6_classification_accepts_valid_years_and_enums(year):
    output = _valid_classification(publication_year=year)
    assert output.syllabus_units == ["Unidade 1"]


@settings(max_examples=100)
@given(year=st.one_of(st.integers(max_value=1899), st.integers(min_value=datetime.now().year + 1, max_value=3000)))
def test_property_7_publication_year_rejects_out_of_range_values(year):
    with pytest.raises(ValidationError):
        _valid_classification(publication_year=year)


@given(unit=st.text(min_size=1).filter(lambda value: value not in {"Unidade 1", "Unidade 2", "Unidade 3"}))
def test_property_6_classification_rejects_invalid_syllabus_units(unit):
    with pytest.raises(ValidationError):
        _valid_classification(syllabus_units=[unit])


@given(topic=st.text(min_size=1).filter(lambda value: value not in TOPICOS_EMENTA))
def test_property_6_classification_rejects_invalid_syllabus_topics(topic):
    with pytest.raises(ValidationError):
        _valid_classification(syllabus_topics=[topic])


def _rubric(score: int = 3, justification: str = "Justificativa com evidência suficiente.") -> RubricScore:
    return RubricScore(score=score, justification=justification)


def _valid_critic(**overrides):
    data = {
        "qualidade_academica": _rubric(),
        "replicabilidade": _rubric(),
        "aplicabilidade_pratica": _rubric(),
        "contribuicao_teorica": _rubric(),
        "adequacao_aluno": _rubric(),
        "contribuicao_aprendizagem": _rubric(),
        "alinhamento_plano": _rubric(),
        "data_availability": "Parcialmente Disponível",
        "replication_links": [],
        "shared_artifacts": ["Nenhum"],
        "resumo_pt": "Resumo curto em português com foco no método e resultado.",
        "main_findings": ["Achado um.", "Achado dois.", "Achado três."],
        "principal_limitation": "Amostra limitada.",
    }
    data.update(overrides)
    return CriticOutput(**data)


@settings(max_examples=100)
@given(score=st.integers(min_value=1, max_value=5), justification=st.text(min_size=20, max_size=500))
def test_property_8_critic_accepts_valid_score_and_justification(score, justification):
    critic = _valid_critic(qualidade_academica=_rubric(score=score, justification=justification))
    assert critic.qualidade_academica.score == score


@given(score=st.one_of(st.integers(max_value=0), st.integers(min_value=6, max_value=100)))
def test_property_8_critic_rejects_score_outside_range(score):
    with pytest.raises(ValidationError):
        _valid_critic(qualidade_academica={"score": score, "justification": "Justificativa com tamanho suficiente."})


def test_property_9_critic_rejects_long_summary_and_wrong_finding_count():
    with pytest.raises(ValidationError):
        _valid_critic(resumo_pt=" ".join(["palavra"] * 151))
    with pytest.raises(ValidationError):
        _valid_critic(main_findings=["um", "dois"])
    with pytest.raises(ValidationError):
        _valid_critic(main_findings=[" ".join(["x"] * 51), "dois", "tres"])


def test_property_10_shared_artifacts_mutual_exclusion():
    assert _valid_critic(shared_artifacts=["Nenhum"]).shared_artifacts == ["Nenhum"]
    with pytest.raises(ValidationError):
        _valid_critic(shared_artifacts=["Código Fonte", "Nenhum"])

