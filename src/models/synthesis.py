from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ThematicRelationship(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relationship_type: Literal["overlap", "continuity", "complementation"]
    description: str = Field(..., min_length=1)
    article_references: list[str] = Field(default_factory=list)


class ThematicCluster(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(..., min_length=1, max_length=60)
    article_references: list[str] = Field(..., min_length=1)


class IFRDDiscussion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    formula_rationale: str = Field(..., min_length=1)
    limitations: list[str] = Field(..., min_length=1)
    viability_conclusion: str = Field(..., min_length=1)


class SynthesisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relationships: list[ThematicRelationship] = Field(default_factory=list)
    clusters: list[ThematicCluster] = Field(default_factory=list)
    ifrd_discussion: IFRDDiscussion
    no_overlap_statement: str | None = None
    no_continuity_statement: str | None = None
    no_complementation_statement: str | None = None

