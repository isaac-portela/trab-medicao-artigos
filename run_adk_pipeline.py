from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from src.config import ARTIGOS_DIR, CHECKPOINTS_DIR, DEFAULT_DELAY, OUTPUT_EXCEL
from src.discovery import discover_articles
from src.excel_exporter import ExcelExporter
from src.orchestrator import PipelineOrchestrator
from src.runtime import CheckpointStore


logger = logging.getLogger("run_adk_pipeline")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline ADK para classificação de artigos acadêmicos.")
    parser.add_argument("--dry-run", action="store_true", help="Processa apenas o primeiro artigo descoberto.")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Delay em segundos entre chamadas DeepSeek.")
    parser.add_argument("--resume", action="store_true", help="Reusa checkpoints existentes e processa apenas faltantes.")
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Mesmo comportamento de --resume: pula artigos com checkpoint existente.",
    )
    parser.add_argument(
        "--article-id",
        action="append",
        default=[],
        help="Filtra por prefixo numérico, nome da pasta ou trecho do título. Pode ser usado várias vezes.",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=CHECKPOINTS_DIR,
        help="Diretório dos checkpoints JSON por artigo.",
    )
    args = parser.parse_args(argv)
    if args.delay < 0:
        parser.error("--delay must be greater than or equal to 0")
    return args


def filter_articles(articles, article_ids: list[str]):
    if not article_ids:
        return articles
    normalized_ids = [value.strip().casefold() for value in article_ids if value.strip()]
    filtered = []
    for article in articles:
        folder_name = article.folder_path.name.casefold()
        title = article.title.casefold()
        numeric_prefix = article.folder_path.name.split(" - ", 1)[0].strip().casefold()
        candidates = [folder_name, title, numeric_prefix]
        if any(any(article_id in candidate for candidate in candidates) for article_id in normalized_ids):
            filtered.append(article)
    return filtered


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


async def async_main(argv: list[str] | None = None) -> int:
    configure_logging()
    load_dotenv(Path.cwd() / ".env")
    args = parse_args(argv)

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print("OPENROUTER_API_KEY is missing or empty.", file=sys.stderr)
        return 1

    articles = discover_articles(ARTIGOS_DIR)
    articles = filter_articles(articles, args.article_id)
    if not articles:
        logger.error("No articles matched the selected filters.")
        return 1
    if args.dry_run:
        logger.info("Dry-run mode enabled: processing only the first article.")
        articles = articles[:1]

    checkpoint_store = CheckpointStore(args.checkpoint_dir)
    progress = tqdm(total=len(articles), desc="Classificando Artigos", unit="artigo")

    def progress_callback(current: int, total: int, title: str) -> None:
        truncated = title[:30] + "..." if len(title) > 30 else title
        progress.set_postfix({"Artigo": truncated, "Atual": f"{current}/{total}"})
        progress.update(1)

    try:
        orchestrator = PipelineOrchestrator(delay_seconds=args.delay, checkpoint_store=checkpoint_store)
        pipeline_result = await orchestrator.run(
            articles,
            progress_callback=progress_callback,
            resume=args.resume,
            only_missing=args.only_missing,
        )
    finally:
        progress.close()

    ExcelExporter.export(pipeline_result.article_results, pipeline_result.synthesis, OUTPUT_EXCEL)
    logger.info("Pipeline completed. Output: %s", OUTPUT_EXCEL.resolve())
    logger.info("Total articles processed: %s", len(pipeline_result.article_results))
    return 0


def main() -> int:
    try:
        return asyncio.run(async_main())
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
