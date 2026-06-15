from __future__ import annotations

import argparse
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ATTACHMENT = Path(
    r"C:\Users\isaac\.codex\attachments\b39153e8-57e8-4769-8ef4-1e8bd698fc69\pasted-text.txt"
)

EXTRA_TEXT = r"""
Pedro Negri Leão Lambert — Assessment of the Level of Software Development Using CMMI-Dev 1.3 on the Unjani Official Web — Link não informado.
João Paulo Aguiar Prado — The DevEx Metrics: Measuring Developer Experience — Link não informado.
André Cota Guimarães — Metrics for Experimentation Programs: Categories, Benefits and Challenges — Link: Agile Processes in Software Engineering and Extreme Programming 26th International Conference on Agile Software Development, XP 2025.
Guilherme Roberto Ferreira Santos — Deep multi-metrics learning for mobile app defect prediction using code and process metrics — Link não informado.
Gustavo Delfino Guimarães — Usage patterns of software product metrics in assessing developers’ output: A comprehensive study — Link não informado.
Jhonatan Gutemberg Rosa Ferreira — Software Quality Measurement Analysis on Academic Information Systems — Link não informado.
Leandro Caldas Pacheco — Software Development Effort Estimation Using Function Points and Simpler Functional Measures: a Comparison — Link: https://ceur-ws.org/Vol-3543/paper8.pdf
Lucas Giovine Madureira Falcone — Empirical Strategies in Software Engineering Research: A Literature Survey — Link não informado.
Lucas Maia Rocha — A/B testing: A systematic literature review — Link não informado.
Miguel Amaral Lessa Xavier — Corporate Dominance in Open Source Ecosystems: A Case Study of OpenStack — Link: https://dl.acm.org/doi/epdf/10.1145/3540250.3549117
Matheus Caetano Rocha — How Many Papers Should You Review? A Research Synthesis of Systematic Literature Reviews in Software Engineering — Link: anexo local não fornecido.
Isaac Portela da Silva — Assessing Quality Through Use: A Usability-Based Evaluation of the Conta gov.br Authentication Platform — Link não informado.
Thiago Borges Laass — Special section: Controlled Experiments in Software Engineering — Link: https://www.sciencedirect.com/science/article/abs/pii/S0950584901002002
Julia Medeiros Silva — Can Developers Prompt? A Controlled Experiment for Code Documentation Generation — Link não informado.
Bernardo Parreiras Prado — Auditable DevOps Automation via VSM and GQM — Link: https://arxiv.org/abs/2601.03574
"""


@dataclass
class Article:
    group: str
    student: str
    title: str
    link: str
    source_line: str


def slug(value: str, max_len: int = 95) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.rstrip(".")
    return value[:max_len].strip() or "sem-titulo"


def parse_lines(text: str, default_group: str) -> list[Article]:
    group = default_group
    articles: list[Article] = []
    headings = {"Lourdes 2026/1", "Lourdes 2025/2", "Coração Eucarístico 2025/2"}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line in headings:
            group = line
            continue
        if " — " not in line:
            continue
        parts = line.split(" — ")
        if len(parts) < 2:
            continue
        student = parts[0].strip()
        title = parts[1].strip()
        link = ""
        if len(parts) >= 3:
            tail = " — ".join(parts[2:])
            match = re.search(r"Link:\s*(.*)$", tail, flags=re.I)
            if match:
                link = match.group(1).strip()
            else:
                link = tail.strip()
        articles.append(Article(group, student, title, link, line))
    return articles


def normalize_pdf_url(article: Article) -> str | None:
    link = article.link.strip()
    if not link or "não informado" in link.lower() or "anexado" in link.lower():
        return None
    url_match = re.search(r"https?://\S+", link)
    if url_match:
        link = url_match.group(0).rstrip(").,")
    manual_hosts = [
        "acm.org",
        "ieeexplore.ieee.org",
        "researchgate.net",
        "sciencedirect.com",
        "scholar.google",
        "periodicos-capes",
    ]
    if any(host in link.lower() for host in manual_hosts):
        return None
    if "doi.org/10.1145/" in link.lower():
        return None
    if "scholar.google" in link.lower() or "periodicos-capes" in link.lower():
        return None
    if link.lower().startswith("science"):
        return None
    if not re.match(r"https?://", link):
        return None

    parsed = urllib.parse.urlparse(link)
    lower = link.lower()
    if lower.endswith(".pdf"):
        return link
    if "arxiv.org/abs/" in lower:
        return link.replace("/abs/", "/pdf/") + ("" if lower.endswith(".pdf") else ".pdf")
    if "doi.org/10.48550/arxiv." in lower:
        arxiv_id = link.rsplit("/", 1)[-1].replace("arXiv.", "")
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    if "mdpi.com/" in lower and "/pdf" not in lower:
        return link.rstrip("/") + "/pdf?download=1"
    if "nature.com/articles/" in lower and not lower.endswith(".pdf"):
        return link.rstrip("/") + ".pdf"
    if "link.springer.com/article/" in lower:
        doi = link.split("/article/", 1)[1]
        return "https://link.springer.com/content/pdf/" + doi + ".pdf"
    if "onlinelibrary.wiley.com/doi/" in lower:
        return link.replace("/doi/", "/doi/pdf/")
    if "doi.org/" in lower and "doi.org/10.48550/arxiv." not in lower:
        return None
    return link if parsed.scheme in {"http", "https"} else None


def looks_like_pdf(path: Path) -> bool:
    try:
        return path.read_bytes()[:4] == b"%PDF"
    except OSError:
        return False


def fetch(url: str, dest: Path) -> tuple[bool, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8",
    }
    ctx = ssl.create_default_context()
    safe_url = urllib.parse.quote(url, safe=":/?&=%#.-_+~")
    req = urllib.request.Request(safe_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            data = response.read()
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"

    tmp = dest.with_suffix(".tmp")
    tmp.write_bytes(data)
    is_pdf = data[:4] == b"%PDF" or "pdf" in content_type.lower()
    if not is_pdf:
        html = data[:500000].decode("utf-8", errors="ignore")
        candidates = []
        for pattern in [
            r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']',
            r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        ]:
            candidates.extend(re.findall(pattern, html, flags=re.I))
        tmp.unlink(missing_ok=True)
        for candidate in candidates[:5]:
            candidate = urllib.parse.urljoin(final_url, candidate.replace("&amp;", "&"))
            ok, nested_note = fetch(candidate, dest)
            if ok:
                return True, nested_note
        tmp.unlink(missing_ok=True)
        return False, f"resposta nao parece PDF ({content_type or 'sem content-type'}; final={final_url})"
    tmp.replace(dest)
    return True, f"baixado de {final_url}"


def status_for(article: Article, pdf_url: str | None, downloaded: bool, note: str) -> str:
    link_l = article.link.lower()
    if downloaded:
        return "x"
    if "acm.org" in link_l:
        return " "
    if "não informado" in link_l or not article.link:
        return " "
    if "anexado" in link_l:
        return " "
    if pdf_url is None:
        return " "
    return " "


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="artigos")
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()

    base = Path(args.out)
    base.mkdir(exist_ok=True)

    source_text = ATTACHMENT.read_text(encoding="utf-8")
    articles = parse_lines(source_text, "Arquivo anexado") + parse_lines(EXTRA_TEXT, "Postagem adicional")

    seen: set[tuple[str, str]] = set()
    unique: list[Article] = []
    for article in articles:
        key = (article.student.casefold(), article.title.casefold())
        if key not in seen:
            seen.add(key)
            unique.append(article)

    rows: list[dict[str, str]] = []
    for index, article in enumerate(unique, start=1):
        group_dir = base / slug(article.group)
        article_dir = group_dir / f"{index:02d} - {slug(article.title)}"
        article_dir.mkdir(parents=True, exist_ok=True)

        info = (
            f"# {article.title}\n\n"
            f"- Aluno: {article.student}\n"
            f"- Grupo: {article.group}\n"
            f"- Link original: {article.link or 'nao informado'}\n"
            f"- Linha fonte: {article.source_line}\n"
        )
        (article_dir / "info.md").write_text(info, encoding="utf-8")

        pdf_url = normalize_pdf_url(article)
        pdf_path = article_dir / "artigo.pdf"
        downloaded = pdf_path.exists() and looks_like_pdf(pdf_path)
        note = "ja existia" if downloaded else ""
        if pdf_url and not downloaded:
            downloaded, note = fetch(pdf_url, pdf_path)
            time.sleep(args.sleep)
        elif not pdf_url:
            note = "sem URL direta de PDF ou fonte manual"

        rows.append(
            {
                "done": status_for(article, pdf_url, downloaded, note),
                "student": article.student,
                "title": article.title,
                "group": article.group,
                "folder": str(article_dir),
                "link": article.link or "nao informado",
                "attempt": pdf_url or "nao tentado",
                "note": note,
            }
        )

    task_lines = [
        "# Tarefas de download dos artigos",
        "",
        "Marcados com `[x]` foram baixados em `artigo.pdf`. Itens `[ ]` precisam de download manual, geralmente por ACM/paywall, link ausente ou página sem PDF direto.",
        "",
    ]
    for row in rows:
        task_lines.append(f"- [{row['done']}] {row['title']} — {row['student']}")
        task_lines.append(f"  - Grupo: {row['group']}")
        task_lines.append(f"  - Pasta: `{row['folder']}`")
        task_lines.append(f"  - Link: {row['link']}")
        task_lines.append(f"  - Tentativa: {row['attempt']}")
        task_lines.append(f"  - Status: {row['note']}")
    (base / "TASKS_DOWNLOAD.md").write_text("\n".join(task_lines) + "\n", encoding="utf-8")

    summary = {
        "total": len(rows),
        "downloaded": sum(1 for row in rows if row["done"] == "x"),
        "manual": sum(1 for row in rows if row["done"] != "x"),
    }
    print(summary)
    print(base / "TASKS_DOWNLOAD.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
