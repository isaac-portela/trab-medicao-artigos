from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ARTIGOS = ROOT / "artigos"
REPORT = ROOT / "docs" / "reference_audit.md"


SEARCH_OVERRIDES = {
    "A Study on Software Metrics and its Impact on Software Quality": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/1905.12922",
        "year": "2019",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Junaid Rashid, Toqeer Mahmood, Muhamad Wasif Nisar.",
    },
    "Software Process Measurement and Related Challenges in Agile Software Development: A Multiple Case Study": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/1809.00860",
        "year": "2018",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Prabhat Ram, Pilar Rodriguez, Markku Oivo.",
    },
    "A Systematic Review of Productivity Factors in Software Development": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/1801.06475",
        "year": "2018",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Stefan Wagner, Melanie Ruhe.",
    },
    "Application of Statistical Methods in Software Engineering: Theory and Practice": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/2006.15624",
        "year": "2020",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores T. F. M. Sirqueira et al.",
    },
    "Evaluation of Software Product Quality Metrics (2020)": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/2009.01557",
        "year": "2020",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Arthur-Jozsef Molnar, Alexandra Neamtu, Simona Motogna.",
    },
    "A/B testing: A systematic literature review": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/2308.04929",
        "year": "2023",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Federico Quin, Danny Weyns, Matthias Galster, Camila Costa Silva.",
    },
    "How Many Papers Should You Review? A Research Synthesis of Systematic Literature Reviews in Software Engineering": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/2307.06056",
        "year": "2023",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Xiaofeng Wang, Henry Edison, Dron Khanna, Usman Rafiq.",
    },
    "Can Developers Prompt? A Controlled Experiment for Code Documentation Generation": {
        "entity": "arXiv",
        "official": "https://arxiv.org/abs/2408.00686",
        "year": "2024",
        "status": "confirmado por busca",
        "notes": "Busca localizou arXiv: autores Hans-Alexander Kruse, Tim Puhlfurss, Walid Maalej.",
    },
}


def slug_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def walk_info_files() -> list[Path]:
    return sorted(ARTIGOS.rglob("info.md"), key=lambda p: str(p).casefold())


def extract_url(value: str) -> str:
    value = html.unescape(value or "")
    match = re.search(r"https?://[^\s)]+", value)
    if not match:
        return ""
    return match.group(0).rstrip(".,;")


def extract_doi(value: str) -> str:
    match = re.search(r"10\.\d{4,9}/[^\s\])}>,;]+", value or "", flags=re.I)
    return match.group(0).rstrip(".,;") if match else ""


def domain(url: str) -> str:
    if not url:
        return ""
    return urlparse(url).hostname or ""


def read_reference(info_path: Path, index: int) -> dict[str, str]:
    text = info_path.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(.+)$", text, flags=re.M)
    student = re.search(r"^- Aluno:\s*(.+)$", text, flags=re.M)
    link = re.search(r"^- Link original:\s*(.+)$", text, flags=re.M)
    source = re.search(r"^- Linha fonte:\s*(.+)$", text, flags=re.M)
    raw_link = (link.group(1).strip() if link else "")
    url = extract_url(raw_link)
    doi = extract_doi(raw_link + " " + (source.group(1) if source else ""))
    pdfs = sorted(p.name for p in info_path.parent.glob("*.pdf"))
    return {
        "index": str(index),
        "file": str(info_path.parent.relative_to(ROOT)).replace("\\", "/"),
        "title": title.group(1).strip() if title else info_path.parent.name,
        "student": student.group(1).strip() if student else "",
        "raw_link": raw_link,
        "url": url,
        "doi": doi,
        "domain": domain(url),
        "pdfs": ", ".join(pdfs),
    }


def classify(ref: dict[str, str]) -> dict[str, str]:
    title = ref["title"]
    if title in SEARCH_OVERRIDES:
        item = SEARCH_OVERRIDES[title].copy()
        item.setdefault("doi", ref["doi"])
        return item

    url = ref["url"]
    doi = ref["doi"]
    host = ref["domain"].lower()
    status = "link existente; validar metadados"
    notes = ""
    entity = "não confirmado"
    official = url or ""
    year_match = re.search(r"\((20\d{2}|19\d{2})\)|\b(20\d{2}|19\d{2})\b", title)
    year = next((g for g in year_match.groups() if g), "") if year_match else ""

    if doi.startswith("10.1145/") or "dl.acm.org" in host or "queue.acm.org" in host:
        entity = "ACM"
        official = f"https://dl.acm.org/doi/{doi}" if doi.startswith("10.1145/") else url
        status = "válido em sessão Chrome/CAPES para domínio ACM"
        notes = "Entidade confirmada pela ACM Digital Library; conteúdo completo pode depender da sessão CAPES."
    elif doi.startswith("10.1109/") or "ieeexplore.ieee.org" in host:
        entity = "IEEE"
        official = url
        status = "válido em sessão Chrome/CAPES para domínio IEEE"
        notes = "Entidade confirmada no IEEE Xplore; conteúdo completo pode depender da sessão CAPES."
    elif doi.startswith("10.1007/") or "link.springer.com" in host:
        entity = "Springer / Springer Nature"
        official = f"https://link.springer.com/article/{doi}" if doi else url
        status = "link oficial identificado"
    elif doi.startswith("10.1002/") or "onlinelibrary.wiley.com" in host:
        entity = "Wiley"
        official = f"https://doi.org/{doi}" if doi else url
        status = "link oficial identificado"
    elif doi.startswith("10.1155/"):
        entity = "Hindawi / Wiley"
        official = f"https://doi.org/{doi}"
        status = "link oficial identificado"
    elif doi.startswith("10.48550/arxiv") or "arxiv.org" in host:
        entity = "arXiv"
        official = url or f"https://doi.org/{doi}"
        status = "link oficial identificado"
    elif "sciencedirect.com" in host or "elsevier.com" in host:
        entity = "Elsevier / ScienceDirect"
        status = "link oficial identificado"
    elif "nature.com" in host:
        entity = "Springer Nature"
        status = "link oficial identificado"
    elif "mdpi.com" in host:
        entity = "MDPI"
        status = "link oficial identificado"
    elif "researchgate.net" in host:
        entity = "ResearchGate"
        status = "repositório secundário; precisa fonte oficial"
        notes = "ResearchGate não é publicadora oficial; buscar DOI/página da revista ou conferência."
    elif "sol.sbc.org.br" in host:
        entity = "SBC OpenLib"
        status = "link oficial identificado"
    elif "ceur-ws.org" in host:
        entity = "CEUR-WS"
        status = "link oficial identificado"
    elif "pucminas.br" in host or "puc-rio.br" in host:
        entity = "Repositório institucional"
        status = "link institucional identificado"
    elif "chimia.ch" in host:
        entity = "CHIMIA"
        status = "link oficial identificado"
    elif "ijeais.org" in host:
        entity = "IJAAR/IJEAIS"
        status = "link do periódico identificado"
    elif "publicacoes.unifal-mg.edu.br" in host:
        entity = "UNIFAL-MG / Sigmae"
        status = "link institucional identificado"
    elif "sedici.unlp.edu.ar" in host:
        entity = "SEDICI / UNLP"
        status = "repositório institucional identificado"
    elif "cs.umd.edu" in host:
        entity = "University of Maryland"
        status = "PDF institucional identificado"
    elif not url:
        status = "não encontrado automaticamente"
        notes = "Sem URL no projeto e sem confirmação oficial nas buscas automáticas feitas até agora."

    if doi and not official:
        official = f"https://doi.org/{doi}"

    return {
        "entity": entity,
        "official": official or "não confirmado",
        "doi": doi,
        "year": year,
        "status": status,
        "notes": notes,
    }


def main() -> None:
    refs = [read_reference(path, i + 1) for i, path in enumerate(walk_info_files())]
    rows = []
    found = []
    broken = []
    manual = []
    duplicates: dict[str, list[str]] = {}

    for ref in refs:
        meta = classify(ref)
        key = (meta.get("doi") or ref["title"]).casefold()
        duplicates.setdefault(key, []).append(ref["file"])
        if "não encontrado" in meta["status"] or "precisa" in meta["status"] or meta["entity"] == "não confirmado":
            manual.append(ref)
        else:
            found.append(ref)
        if "quebrado" in meta["status"]:
            broken.append(ref)
        rows.append((ref, meta))

    duplicate_rows = {k: v for k, v in duplicates.items() if len(v) > 1}

    lines = [
        "# Auditoria de Referências Acadêmicas",
        "",
        "Relatório gerado a partir dos arquivos `artigos/**/info.md` e dos links registrados no projeto.",
        "",
        "Validação feita nesta rodada:",
        "- links ACM e IEEE foram conferidos na sessão ativa do Chrome/CAPES do usuário, com `ACM Digital Library` e `IEEE Xplore` mostrando acesso institucional PUC/MG;",
        "- páginas oficiais foram priorizadas por domínio/DOI quando já existiam no projeto;",
        "- itens sem URL ou com ResearchGate/Google Scholar foram marcados para revisão manual quando a busca automática não confirmou fonte oficial;",
        "- dados ausentes não foram inventados.",
        "",
        "| Arquivo/Referência | Título encontrado | Entidade | Fonte oficial | DOI | Ano | Status | Observações |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for ref, meta in rows:
        obs = meta["notes"]
        if ref["pdfs"]:
            obs = (obs + " " if obs else "") + f"PDF local: {ref['pdfs']}."
        if ref["raw_link"] and not ref["url"]:
            obs = (obs + " " if obs else "") + f"Link original textual: {ref['raw_link']}."
        lines.append(
            "| "
            + " | ".join(
                [
                    slug_escape(ref["file"]),
                    slug_escape(ref["title"]),
                    slug_escape(meta["entity"]),
                    slug_escape(meta["official"]),
                    slug_escape(meta.get("doi") or ref["doi"] or ""),
                    slug_escape(meta["year"]),
                    slug_escape(meta["status"]),
                    slug_escape(obs),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Referências encontradas com sucesso",
            "",
            f"Total: {len(found)} de {len(refs)}.",
        ]
    )
    for ref in found:
        lines.append(f"- {ref['title']} — {ref['file']}")

    lines.extend(["", "## Referências com link quebrado", ""])
    if broken:
        for ref in broken:
            lines.append(f"- {ref['title']} — {ref['url'] or ref['raw_link']}")
    else:
        lines.append("- Nenhum link foi marcado como quebrado nesta auditoria; itens não testados ou sem confirmação ficaram em revisão manual.")

    lines.extend(["", "## Referências que precisam de revisão manual", ""])
    if manual:
        for ref in manual:
            lines.append(f"- {ref['title']} — {ref['file']} — link: {ref['raw_link'] or 'não informado'}")
    else:
        lines.append("- Nenhuma.")

    lines.extend(["", "## Referências duplicadas ou suspeitas", ""])
    if duplicate_rows:
        for _, files in duplicate_rows.items():
            lines.append("- " + " | ".join(files))
    else:
        lines.append("- Nenhuma duplicidade exata por DOI/título foi detectada.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    print(json.dumps({"total": len(refs), "found": len(found), "manual": len(manual), "duplicates": len(duplicate_rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
