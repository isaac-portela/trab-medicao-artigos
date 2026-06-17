from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from hypothesis import given, settings, strategies as st

from src.discovery import discover_articles, parse_info_md
from src.ifrd import calculate_ifrd, classify_ifrd
from src.services.cache import FileCache
from src.services.citation_lookup import CitationLookupService
from src.services.pdf_extractor import normalize_whitespace


@settings(max_examples=100)
@given(depth=st.integers(min_value=0, max_value=5), has_pdf=st.booleans())
def test_properties_1_and_2_discovery_respects_depth_and_pdf_filter(depth, has_pdf):
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir) / "artigos"
        folder = base
        for index in range(depth):
            folder = folder / f"nivel-{index}"
        folder.mkdir(parents=True)
        (folder / "info.md").write_text("# Título\n\n- Aluno: Ana\n", encoding="utf-8")
        if has_pdf:
            (folder / "artigo.pdf").write_bytes(b"%PDF-1.4\n")

        if depth <= 3 and has_pdf:
            articles = discover_articles(base, max_depth=3)
            assert len(articles) == 1
            assert articles[0].pdf_path == folder / "artigo.pdf"
        else:
            with pytest.raises(ValueError):
                discover_articles(base, max_depth=3)


def test_property_3_info_md_parsing_extracts_fields_with_defaults(tmp_path):
    info = tmp_path / "info.md"
    info.write_text("# Meu Artigo\n\n- Aluno: Maria\n- Link original: https://example.test\n", encoding="utf-8")
    parsed = parse_info_md(info)
    assert parsed == {
        "title": "Meu Artigo",
        "student": "Maria",
        "group": "",
        "link": "https://example.test",
    }


@settings(max_examples=100)
@given(text=st.text())
def test_property_4_whitespace_normalization_has_no_consecutive_whitespace(text):
    normalized = normalize_whitespace(text)
    assert "  " not in normalized
    assert "\n" not in normalized
    assert "\t" not in normalized


@settings(max_examples=100)
@given(
    qualidade=st.integers(min_value=1, max_value=5),
    alinhamento=st.integers(min_value=1, max_value=5),
    aprendizagem=st.integers(min_value=1, max_value=5),
    replicabilidade=st.integers(min_value=1, max_value=5),
    aplicabilidade=st.integers(min_value=1, max_value=5),
    adequacao=st.integers(min_value=1, max_value=5),
)
def test_property_13_ifrd_formula_and_classification(
    qualidade,
    alinhamento,
    aprendizagem,
    replicabilidade,
    aplicabilidade,
    adequacao,
):
    scores = {
        "qualidade_academica": qualidade,
        "alinhamento_plano": alinhamento,
        "contribuicao_aprendizagem": aprendizagem,
        "replicabilidade": replicabilidade,
        "aplicabilidade_pratica": aplicabilidade,
        "adequacao_aluno": adequacao,
    }
    expected = round(
        0.25 * qualidade
        + 0.20 * alinhamento
        + 0.20 * aprendizagem
        + 0.15 * replicabilidade
        + 0.10 * aplicabilidade
        + 0.10 * adequacao,
        2,
    )
    assert calculate_ifrd(scores) == expected
    label, _ = classify_ifrd(expected)
    assert label == ("Bom Artigo" if expected >= 4 else "Intermediário" if expected >= 3 else "Fraco")


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params, timeout))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_property_11_citation_fallback_crossref_to_semantic(tmp_path, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _: None)
    session = FakeSession(
        [
            FakeResponse({"message": {"items": [{}]}}),
            FakeResponse({"data": [{"citationCount": 12}]}),
        ]
    )
    service = CitationLookupService(cache_path=tmp_path / "cache.json", session=session, min_interval_seconds=0)
    result = service.get_citation_count("A title")
    assert result.count == 12
    assert result.source == "semantic_scholar"
    assert len(session.calls) == 2


def test_property_12_cache_round_trip_and_ttl(tmp_path):
    cache_path = tmp_path / "cache.json"
    cache = FileCache(cache_path, ttl_days=7)
    cache.set("paper", 42)
    assert FileCache(cache_path, ttl_days=7).get("paper") == 42

    stale = {
        "paper": {
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=8)).isoformat(),
            "value": 42,
        }
    }
    import json

    cache_path.write_text(json.dumps(stale), encoding="utf-8")
    assert FileCache(cache_path, ttl_days=7).get("paper") is None
