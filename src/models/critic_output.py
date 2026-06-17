from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


DataAvailability = Literal["Totalmente Disponível", "Parcialmente Disponível", "Não Disponível"]
SharedArtifact = Literal["Código Fonte", "Dataset", "Scripts R/Python", "Questionários", "Nenhum"]


def _word_count(value: str) -> int:
    return len(value.split())


class RubricScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(..., ge=1, le=5)
    justification: str = Field(..., min_length=20, max_length=500)


class CriticOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    qualidade_academica: RubricScore
    replicabilidade: RubricScore
    aplicabilidade_pratica: RubricScore
    contribuicao_teorica: RubricScore
    adequacao_aluno: RubricScore
    contribuicao_aprendizagem: RubricScore
    alinhamento_plano: RubricScore
    data_availability: DataAvailability
    replication_links: list[str] = Field(default_factory=list)
    shared_artifacts: list[SharedArtifact] = Field(..., min_length=1)
    resumo_pt: str = Field(..., min_length=1)
    main_findings: list[str] = Field(..., min_length=3, max_length=3)
    principal_limitation: str = Field(..., min_length=1, max_length=250)

    @field_validator("shared_artifacts")
    @classmethod
    def validate_shared_artifacts_mutual_exclusion(cls, values: list[str]) -> list[str]:
        if "Nenhum" in values and len(values) > 1:
            raise ValueError("'Nenhum' must be the only shared artifact when present")
        return values

    @field_validator("resumo_pt")
    @classmethod
    def validate_summary_word_count(cls, value: str) -> str:
        if _word_count(value) > 150:
            raise ValueError("resumo_pt exceeds 150 words")
        return value

    @field_validator("main_findings")
    @classmethod
    def validate_findings_word_count(cls, values: list[str]) -> list[str]:
        if any(_word_count(value) > 50 for value in values):
            raise ValueError("each main finding must contain at most 50 words")
        return values

    @field_validator("principal_limitation")
    @classmethod
    def validate_limitation_word_count(cls, value: str) -> str:
        if _word_count(value) > 50:
            raise ValueError("principal_limitation exceeds 50 words")
        return value

    def rubric_scores(self) -> dict[str, int]:
        return {
            "qualidade_academica": self.qualidade_academica.score,
            "replicabilidade": self.replicabilidade.score,
            "aplicabilidade_pratica": self.aplicabilidade_pratica.score,
            "contribuicao_teorica": self.contribuicao_teorica.score,
            "adequacao_aluno": self.adequacao_aluno.score,
            "contribuicao_aprendizagem": self.contribuicao_aprendizagem.score,
            "alinhamento_plano": self.alinhamento_plano.score,
        }

