from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SuperSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    core_research_question: str = Field(..., min_length=1)
    methodology_description: str = Field(..., min_length=1)
    key_findings: list[str] = Field(..., min_length=1, max_length=10)
    statistical_techniques: list[str] = Field(default_factory=list)

    @field_validator("core_research_question", "methodology_description")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field cannot be blank")
        return value

    @field_validator("key_findings", "statistical_techniques")
    @classmethod
    def validate_string_items(cls, values: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values]
        if any(not item for item in cleaned):
            raise ValueError("list items cannot be blank")
        return cleaned

