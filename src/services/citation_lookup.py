from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from src.config import CACHE_PATH, CACHE_TTL_DAYS

from .cache import FileCache


@dataclass(frozen=True)
class CitationResult:
    count: int | None
    source: str
    error_message: str | None = None


class CitationLookupService:
    def __init__(
        self,
        cache_path: Path = CACHE_PATH,
        cache_ttl_days: int = CACHE_TTL_DAYS,
        timeout_seconds: int = 10,
        retries: int = 2,
        retry_delay_seconds: float = 2.0,
        min_interval_seconds: float = 1.0,
        session: requests.Session | None = None,
    ):
        self.cache = FileCache(cache_path, ttl_days=cache_ttl_days)
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.retry_delay_seconds = retry_delay_seconds
        self.min_interval_seconds = min_interval_seconds
        self.session = session or requests.Session()
        self._last_request_at: dict[str, float] = {}

    def get_citation_count(self, title: str) -> CitationResult:
        title = title.strip()
        if not title:
            return CitationResult(count=None, source="N/A", error_message="empty title")

        cached = self.cache.get(title)
        if cached is not None:
            return CitationResult(count=cached, source="cache")

        errors: list[str] = []
        crossref = self._query_crossref(title)
        if crossref.count is not None:
            self.cache.set(title, crossref.count)
            return crossref
        if crossref.error_message:
            errors.append(crossref.error_message)

        semantic = self._query_semantic_scholar(title)
        if semantic.count is not None:
            self.cache.set(title, semantic.count)
            return semantic
        if semantic.error_message:
            errors.append(semantic.error_message)

        self.cache.set(title, None)
        return CitationResult(count=None, source="N/A", error_message="; ".join(errors) or None)

    def _request_json(self, api_name: str, url: str, params: dict[str, Any]) -> dict[str, Any] | None:
        last_request = self._last_request_at.get(api_name, 0.0)
        wait = self.min_interval_seconds - (time.monotonic() - last_request)
        if wait > 0:
            time.sleep(wait)

        for attempt in range(self.retries + 1):
            try:
                self._last_request_at[api_name] = time.monotonic()
                response = self.session.get(url, params=params, timeout=self.timeout_seconds)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError):
                if attempt >= self.retries:
                    return None
                time.sleep(self.retry_delay_seconds)
        return None

    def _query_crossref(self, title: str) -> CitationResult:
        payload = self._request_json(
            "crossref",
            "https://api.crossref.org/works",
            {"query.title": title, "rows": 1},
        )
        try:
            items = payload["message"]["items"] if payload else []
            if not items:
                return CitationResult(count=None, source="crossref")
            count = items[0].get("is-referenced-by-count")
            return CitationResult(count=count if isinstance(count, int) else None, source="crossref")
        except (KeyError, TypeError, IndexError):
            return CitationResult(count=None, source="crossref", error_message="invalid CrossRef response")

    def _query_semantic_scholar(self, title: str) -> CitationResult:
        payload = self._request_json(
            "semantic_scholar",
            "https://api.semanticscholar.org/graph/v1/paper/search",
            {"query": title, "limit": 1, "fields": "citationCount"},
        )
        try:
            data = payload.get("data", []) if payload else []
            if not data:
                return CitationResult(count=None, source="semantic_scholar")
            count = data[0].get("citationCount")
            return CitationResult(
                count=count if isinstance(count, int) else None,
                source="semantic_scholar",
            )
        except (AttributeError, TypeError, IndexError):
            return CitationResult(
                count=None,
                source="semantic_scholar",
                error_message="invalid Semantic Scholar response",
            )

