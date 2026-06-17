from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .classification import ClassificationOutput
from .super_summary import SuperSummary


class ArticleMetadataDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    folder_path: str
    title: str
    student: str
    group: str
    link: str


class ReaderInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metadata: ArticleMetadataDTO
    extracted_text: str = ""
    pdf_extraction_failed: bool = False


class ClassifierInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metadata: ArticleMetadataDTO
    super_summary: SuperSummary | None = None


class CriticInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metadata: ArticleMetadataDTO
    super_summary: SuperSummary | None = None
    classification: ClassificationOutput


class ArticleResultSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    folder_name: str
    title: str
    theme: str | None = None
    syllabus_units: list[str] = Field(default_factory=list)
    syllabus_topics: list[str] = Field(default_factory=list)
    super_summary: SuperSummary | None = None
    rubric_scores: dict[str, int] | None = None


class SynthesizerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    articles: list[ArticleResultSummary]

