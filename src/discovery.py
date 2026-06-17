from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArticleMetadata:
    folder_path: Path
    title: str
    student: str
    group: str
    link: str
    pdf_path: Path


def _relative_depth(path: Path, base_dir: Path) -> int:
    return len(path.parent.relative_to(base_dir).parts)


def parse_info_md(info_path: Path) -> dict[str, str]:
    content = info_path.read_text(encoding="utf-8")
    fields = {"title": "", "student": "", "group": "", "link": ""}

    title_match = re.search(r"^\s*#\s+(.+?)\s*$", content, flags=re.MULTILINE)
    if title_match:
        fields["title"] = title_match.group(1).strip()

    patterns = {
        "student": r"^\s*[-*]?\s*Aluno\s*:\s*(.*?)\s*$",
        "group": r"^\s*[-*]?\s*Grupo\s*:\s*(.*?)\s*$",
        "link": r"^\s*[-*]?\s*Link original\s*:\s*(.*?)\s*$",
    }
    for field, pattern in patterns.items():
        match = re.search(pattern, content, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            fields[field] = match.group(1).strip()
    return fields


def discover_articles(base_dir: Path, max_depth: int = 3) -> list[ArticleMetadata]:
    if not base_dir.exists() or not base_dir.is_dir():
        raise FileNotFoundError(f"Article directory not found: {base_dir}")

    info_files = [
        path
        for path in base_dir.rglob("info.md")
        if path.is_file() and _relative_depth(path, base_dir) <= max_depth
    ]
    if not info_files:
        raise ValueError(f"No article folders found under: {base_dir}")

    articles: list[ArticleMetadata] = []
    for info_path in sorted(info_files, key=lambda path: str(path).casefold()):
        pdf_path = info_path.parent / "artigo.pdf"
        if not pdf_path.is_file():
            continue
        metadata = parse_info_md(info_path)
        articles.append(
            ArticleMetadata(
                folder_path=info_path.parent,
                title=metadata["title"],
                student=metadata["student"],
                group=metadata["group"],
                link=metadata["link"],
                pdf_path=pdf_path,
            )
        )

    if not articles:
        raise ValueError(f"No article folders with both info.md and artigo.pdf found under: {base_dir}")
    return articles

