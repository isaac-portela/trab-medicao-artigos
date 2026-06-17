from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class FileCache:
    def __init__(self, path: Path, ttl_days: int = 7):
        self.path = path
        self.ttl = timedelta(days=ttl_days)
        self._data: dict[str, dict[str, Any]] = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        try:
            content = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return content if isinstance(content, dict) else {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def get(self, key: str) -> Any | None:
        entry = self._data.get(key)
        if not entry:
            return None
        timestamp_raw = entry.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_raw)
        except (TypeError, ValueError):
            return None
        if self._now() - timestamp > self.ttl:
            return None
        return entry.get("value")

    def set(self, key: str, value: Any) -> None:
        self._data[key] = {"timestamp": self._now().isoformat(), "value": value}
        self._save()

