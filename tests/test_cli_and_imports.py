from __future__ import annotations

import pytest

from run_adk_pipeline import filter_articles, parse_args
from src.config import ARTIGOS_DIR
from src.discovery import discover_articles
from src.orchestrator import PipelineOrchestrator


def test_cli_rejects_negative_delay():
    with pytest.raises(SystemExit):
        parse_args(["--delay", "-0.1"])


def test_cli_accepts_dry_run_and_delay():
    args = parse_args(["--dry-run", "--delay", "0", "--resume", "--article-id", "01"])
    assert args.dry_run is True
    assert args.delay == 0
    assert args.resume is True
    assert args.article_id == ["01"]


def test_orchestrator_class_is_importable():
    assert PipelineOrchestrator.__name__ == "PipelineOrchestrator"


def test_real_workspace_discovers_pdf_articles():
    articles = discover_articles(ARTIGOS_DIR)
    assert len(articles) > 0
    assert all(article.pdf_path.name == "artigo.pdf" for article in articles)


def test_article_id_filter_matches_numeric_prefix_title_or_folder():
    articles = discover_articles(ARTIGOS_DIR)
    first = articles[0]
    numeric_prefix = first.folder_path.name.split(" - ", 1)[0]
    assert filter_articles(articles, [numeric_prefix]) == [first]
    assert first in filter_articles(articles, [first.title[:12]])
    assert first in filter_articles(articles, [first.folder_path.name[:12]])
