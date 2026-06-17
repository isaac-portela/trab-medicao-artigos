from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.config import TOPICOS_EMENTA, UNIDADES


VenueType = Literal[
    "Revista (Journal)",
    "Conferência (Conference)",
    "Repositório (arXiv/Preprint)",
    "Outro",
]
StudyType = Literal[
    "Experimento Controlado",
    "Quase-experimento",
    "Estudo de Caso",
    "Survey",
    "Revisão Sistemática",
    "Proposta Conceitual",
    "Outro",
]
ResearchNature = Literal["Prática (Empírica)", "Teórica", "Híbrida"]
DataNature = Literal["Quantitativa", "Qualitativa", "Mista"]


class ClassificationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theme: str = Field(..., min_length=1)
    publication_year: int | None = None
    publisher_entity: str = Field(..., min_length=1)
    venue_type: VenueType
    study_type: StudyType
    research_nature: ResearchNature
    data_nature: DataNature
    sample_size: str = Field(..., min_length=1)
    statistical_methods: list[str] = Field(default_factory=list)
    software_metrics: list[str] = Field(default_factory=list)
    syllabus_units: list[str] = Field(..., min_length=1)
    syllabus_topics: list[str] = Field(..., min_length=1)

    @field_validator("publication_year")
    @classmethod
    def validate_publication_year(cls, value: int | None) -> int | None:
        if value is None:
            return value
        current_year = datetime.now().year
        if value < 1900 or value > current_year:
            raise ValueError(f"publication_year must be between 1900 and {current_year}, or None")
        return value

    @field_validator("syllabus_units")
    @classmethod
    def validate_units(cls, values: list[str]) -> list[str]:
        invalid = [value for value in values if value not in UNIDADES]
        if invalid:
            raise ValueError(f"invalid syllabus_units: {invalid}")
        return values

    @field_validator("syllabus_topics")
    @classmethod
    def validate_topics(cls, values: list[str]) -> list[str]:
        invalid = [value for value in values if value not in TOPICOS_EMENTA]
        if invalid:
            raise ValueError(f"invalid syllabus_topics: {invalid}")
        return values

