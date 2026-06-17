from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pypdf


@dataclass(frozen=True)
class ExtractionResult:
    text: str
    success: bool
    error_message: str | None = None


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_pdf_text(pdf_path: Path, max_chars: int = 80_000) -> ExtractionResult:
    if not pdf_path.is_file():
        return ExtractionResult(text="", success=False, error_message=f"PDF file not found: {pdf_path}")

    try:
        reader = pypdf.PdfReader(str(pdf_path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return ExtractionResult(text="", success=False, error_message=f"Encrypted PDF: {pdf_path}")

        pages: list[str] = []
        total_chars = 0
        for page in reader.pages:
            page_text = normalize_whitespace(page.extract_text() or "")
            if not page_text:
                continue
            pages.append(page_text)
            total_chars += len(page_text) + 1
            if total_chars >= max_chars:
                break
        return ExtractionResult(text=" ".join(pages)[:max_chars], success=True)
    except Exception as exc:
        return ExtractionResult(
            text="",
            success=False,
            error_message=f"PDF extraction failed for {pdf_path}: {type(exc).__name__}: {exc}",
        )

