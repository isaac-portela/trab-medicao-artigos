from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.discovery import ArticleMetadata
from src.models import ArticleResult, ClassificationOutput, CriticOutput, ProcessingStatus, SuperSummary


class CheckpointStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def article_key(self, metadata: ArticleMetadata) -> str:
        return self._safe_name(metadata.folder_path.name)

    def path_for(self, metadata: ArticleMetadata) -> Path:
        return self.base_dir / f"{self.article_key(metadata)}.json"

    def exists(self, metadata: ArticleMetadata) -> bool:
        return self.path_for(metadata).is_file()

    def load(self, metadata: ArticleMetadata) -> ArticleResult | None:
        path = self.path_for(metadata)
        if not path.is_file():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

        outputs = payload.get("outputs", {})
        try:
            status = ProcessingStatus(payload["processing_status"])
            super_summary = self._model_or_none(SuperSummary, outputs.get("super_summary"))
            classification = self._model_or_none(ClassificationOutput, outputs.get("classification"))
            critic_output = self._model_or_none(CriticOutput, outputs.get("critic_output"))
            return ArticleResult(
                metadata=metadata,
                processing_status=status,
                super_summary=super_summary,
                classification=classification,
                critic_output=critic_output,
                citation_count=outputs.get("citation_count"),
                ifrd=outputs.get("ifrd"),
                error=payload.get("error"),
                citation_source=outputs.get("citation_source"),
            )
        except (KeyError, ValueError, TypeError):
            return None

    def save(self, result: ArticleResult) -> Path:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        path = self.path_for(result.metadata)
        payload = self._payload_for_result(result)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _payload_for_result(self, result: ArticleResult) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "article_key": self.article_key(result.metadata),
            "metadata": {
                "folder_path": str(result.metadata.folder_path),
                "folder_name": result.metadata.folder_path.name,
                "title": result.metadata.title,
                "student": result.metadata.student,
                "group": result.metadata.group,
                "link": result.metadata.link,
                "pdf_path": str(result.metadata.pdf_path),
            },
            "processing_status": result.processing_status.value,
            "error": result.error,
            "outputs": {
                "super_summary": self._dump_model(result.super_summary),
                "classification": self._dump_model(result.classification),
                "critic_output": self._dump_model(result.critic_output),
                "citation_count": result.citation_count,
                "citation_source": result.citation_source,
                "ifrd": result.ifrd,
            },
        }

    @staticmethod
    def _dump_model(model: Any) -> dict[str, Any] | None:
        return model.model_dump(mode="json") if model is not None else None

    @staticmethod
    def _model_or_none(model_type, data):
        return model_type.model_validate(data) if data is not None else None

    @staticmethod
    def _safe_name(value: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
        safe = re.sub(r"_+", "_", safe).strip("._")
        return safe[:140] or "article"
