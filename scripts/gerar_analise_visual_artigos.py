from __future__ import annotations

import argparse
import math
import re
import textwrap
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
except ModuleNotFoundError as exc:  # pragma: no cover - friendly runtime failure
    raise SystemExit(
        "Dependencia ausente: matplotlib. Execute `pip install -r requirements.txt` "
        "no ambiente virtual do projeto e rode o script novamente."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "classificacao_artigos.xlsx"
DEFAULT_OUTPUT = ROOT / "outputs" / "apresentacao_artigos"

MAIN_SHEET = "Artigos Classificados"
SYNTHESIS_SHEET = "Síntese Temática"

RUBRIC_COLUMNS = {
    "Nota: Qualidade": "Qualidade",
    "Nota: Replicabilidade": "Replicabilidade",
    "Nota: Aplicabilidade": "Aplicabilidade",
    "Nota: Contribuição Teórica": "Contrib. Teórica",
    "Nota: Adequação": "Adequação",
    "Nota: Aprendizagem": "Aprendizagem",
    "Nota: Alinhamento": "Alinhamento",
}

SLIDE_COLORS = [
    "#2563EB",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#06B6D4",
    "#64748B",
    "#84CC16",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Gera tabelas derivadas e graficos para a apresentacao do estudo "
            "observacional dos artigos."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Arquivo Excel de entrada.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Pasta de saida.")
    parser.add_argument("--top-n", type=int, default=15, help="Quantidade padrao para rankings.")
    parser.add_argument("--dpi", type=int, default=220, help="Resolucao dos PNGs.")
    return parser.parse_args()


def setup_plot_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#CBD5E1",
            "axes.labelcolor": "#0F172A",
            "axes.titlecolor": "#0F172A",
            "axes.titlesize": 22,
            "axes.labelsize": 16,
            "xtick.labelsize": 13,
            "ytick.labelsize": 13,
            "legend.fontsize": 13,
            "font.size": 14,
            "grid.color": "#E2E8F0",
            "grid.linewidth": 1.0,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )


def clean_label(value: object, max_chars: int = 48) -> str:
    if pd.isna(value):
        return "N/A"
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) <= max_chars:
        return text
    return textwrap.shorten(text, width=max_chars, placeholder="...")


def split_multivalue(series: pd.Series) -> list[str]:
    values: list[str] = []
    for raw in series.dropna():
        for item in str(raw).split("\n"):
            item = item.strip()
            if item:
                values.append(item)
    return values


def normalize_count_column(df: pd.DataFrame, col: str) -> pd.Series:
    series = pd.to_numeric(df[col].replace({"N/A": np.nan, "nan": np.nan}), errors="coerce")
    return series.fillna(0)


def ensure_dirs(output_dir: Path) -> dict[str, Path]:
    dirs = {
        "root": output_dir,
        "charts": output_dir / "graficos",
        "csv": output_dir / "tabelas_csv",
        "md": output_dir / "tabelas_md",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Tabela vazia._"
    printable = df.copy()
    printable = printable.fillna("")
    printable = printable.astype(str)
    headers = [str(col) for col in printable.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in printable.iterrows():
        cells = [str(value).replace("\n", "<br>").replace("|", "\\|") for value in row.tolist()]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def save_table(df: pd.DataFrame, name: str, dirs: dict[str, Path]) -> None:
    csv_path = dirs["csv"] / f"{name}.csv"
    md_path = dirs["md"] / f"{name}.md"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    md_path.write_text(markdown_table(df), encoding="utf-8")


def save_fig(fig: plt.Figure, path: Path, dpi: int) -> None:
    fig.savefig(path, dpi=dpi)
    plt.close(fig)


def set_chart_header(ax, title: str, subtitle: str) -> None:
    ax.set_title(f"{title}\n", loc="left", pad=24, fontweight="bold")
    ax.text(
        0,
        1.012,
        subtitle,
        transform=ax.transAxes,
        fontsize=14,
        color="#475569",
        va="bottom",
    )


def add_bar_labels(ax, fmt: str = "{:.0f}", padding: float = 0.04) -> None:
    x_min, x_max = ax.get_xlim()
    span = max(x_max - x_min, 1)
    for patch in ax.patches:
        width = patch.get_width()
        y = patch.get_y() + patch.get_height() / 2
        ax.text(
            width + span * padding,
            y,
            fmt.format(width),
            va="center",
            ha="left",
            fontsize=13,
            color="#0F172A",
            fontweight="bold",
        )


def plot_horizontal_bar(
    series: pd.Series,
    title: str,
    subtitle: str,
    output_path: Path,
    dpi: int,
    xlabel: str = "Quantidade",
    color: str = "#2563EB",
    value_fmt: str = "{:.0f}",
) -> None:
    series = series.dropna()
    fig, ax = plt.subplots(figsize=(16, 9))
    y_labels = [clean_label(v, 64) for v in series.index]
    ax.barh(y_labels, series.values, color=color, height=0.62)
    ax.invert_yaxis()
    ax.grid(axis="x")
    ax.set_xlabel(xlabel)
    set_chart_header(ax, title, subtitle)
    ax.spines[["top", "right", "left"]].set_visible(False)
    add_bar_labels(ax, value_fmt)
    ax.set_xlim(0, max(series.values) * 1.18 if len(series) else 1)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_vertical_bar(
    series: pd.Series,
    title: str,
    subtitle: str,
    output_path: Path,
    dpi: int,
    ylabel: str = "Quantidade",
) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    labels = [clean_label(v, 26) for v in series.index]
    bars = ax.bar(labels, series.values, color=SLIDE_COLORS[: len(series)])
    ax.grid(axis="y")
    ax.set_ylabel(ylabel)
    set_chart_header(ax, title, subtitle)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", rotation=18)
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + max(series.values) * 0.025,
            f"{height:.0f}",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )
    ax.set_ylim(0, max(series.values) * 1.16 if len(series) else 1)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_donut(series: pd.Series, title: str, subtitle: str, output_path: Path, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    values = series.values
    labels = [clean_label(v, 42) for v in series.index]
    total = values.sum()
    wedges, _ = ax.pie(
        values,
        colors=SLIDE_COLORS[: len(series)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "white", "linewidth": 3},
    )
    ax.text(0, 0.03, f"{int(total)}", ha="center", va="center", fontsize=38, fontweight="bold")
    ax.text(0, -0.15, "artigos", ha="center", va="center", fontsize=16, color="#475569")
    legend_labels = [f"{label}: {value:.0f} ({value / total:.0%})" for label, value in zip(labels, values)]
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(0.82, 0.5), frameon=False)
    set_chart_header(ax, title, subtitle)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_radar(rubric_means: pd.Series, output_path: Path, dpi: int) -> None:
    labels = rubric_means.index.tolist()
    values = rubric_means.values.tolist()
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(14, 10), subplot_kw={"polar": True})
    ax.plot(angles, values, color="#2563EB", linewidth=3)
    ax.fill(angles, values, color="#2563EB", alpha=0.18)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#64748B")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=14)
    ax.set_title("Médias das rubricas de avaliação\n", loc="left", pad=35, fontweight="bold")
    fig.text(
        0.08,
        0.89,
        "Escala de 1 a 5; mostra forças e fragilidades do corpus.",
        fontsize=14,
        color="#475569",
    )
    save_fig(fig, output_path, dpi)


def plot_histogram(df: pd.DataFrame, output_path: Path, dpi: int) -> None:
    values = pd.to_numeric(df["IFRD"], errors="coerce").dropna()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.hist(values, bins=np.arange(2.0, 5.05, 0.25), color="#2563EB", edgecolor="white", linewidth=1.5)
    mean = values.mean()
    median = values.median()
    ax.axvline(mean, color="#EF4444", linewidth=3, label=f"Média: {mean:.2f}")
    ax.axvline(median, color="#10B981", linewidth=3, linestyle="--", label=f"Mediana: {median:.2f}")
    ax.grid(axis="y")
    ax.set_xlabel("IFRD")
    ax.set_ylabel("Quantidade de artigos")
    set_chart_header(
        ax,
        "Distribuição do IFRD",
        "O IFRD resume qualidade, alinhamento, aprendizagem, replicabilidade, aplicabilidade e adequação.",
    )
    ax.legend(loc="upper left", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_boxplot(df: pd.DataFrame, output_path: Path, dpi: int) -> None:
    grouped = []
    labels = []
    ordered = df.groupby("Tipo Estudo")["IFRD"].median().sort_values(ascending=False).index.tolist()
    for label in ordered:
        values = pd.to_numeric(df.loc[df["Tipo Estudo"] == label, "IFRD"], errors="coerce").dropna()
        if len(values) >= 2:
            grouped.append(values.values)
            labels.append(clean_label(label, 24))
    fig, ax = plt.subplots(figsize=(16, 9))
    bp = ax.boxplot(grouped, patch_artist=True, tick_labels=labels, showmeans=True)
    for patch, color in zip(bp["boxes"], SLIDE_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    for median in bp["medians"]:
        median.set_color("#0F172A")
        median.set_linewidth(2)
    ax.grid(axis="y")
    ax.set_ylabel("IFRD")
    ax.set_ylim(1.8, 5.1)
    set_chart_header(ax, "IFRD por tipo de estudo", "Compara a dispersão do indicador final entre desenhos metodológicos.")
    ax.tick_params(axis="x", rotation=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_scatter_citations(df: pd.DataFrame, output_path: Path, dpi: int) -> None:
    data = df.copy()
    data["Citações Num"] = normalize_count_column(data, "Citações")
    data["IFRD"] = pd.to_numeric(data["IFRD"], errors="coerce")
    data = data.dropna(subset=["IFRD"])
    fig, ax = plt.subplots(figsize=(16, 9))
    categories = data["Classificação IFRD"].fillna("N/A").unique().tolist()
    palette = dict(zip(categories, SLIDE_COLORS))
    for category in categories:
        subset = data[data["Classificação IFRD"].fillna("N/A") == category]
        ax.scatter(
            subset["Citações Num"],
            subset["IFRD"],
            s=95,
            alpha=0.75,
            label=category,
            color=palette[category],
            edgecolor="white",
            linewidth=0.8,
        )
    ax.set_xscale("symlog", linthresh=1)
    ax.grid(True)
    ax.set_xlabel("Citações (escala simétrica log)")
    ax.set_ylabel("IFRD")
    ax.set_ylim(1.8, 5.1)
    set_chart_header(ax, "Citações versus IFRD", "Ajuda a discutir se impacto bibliométrico acompanha aderência didática.")
    ax.legend(title="Classificação IFRD", frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_correlation_heatmap(df: pd.DataFrame, output_path: Path, dpi: int) -> None:
    corr = df[list(RUBRIC_COLUMNS)].apply(pd.to_numeric, errors="coerce").corr()
    labels = [RUBRIC_COLUMNS[col] for col in corr.columns]
    fig, ax = plt.subplots(figsize=(14, 11))
    im = ax.imshow(corr.values, cmap="Blues", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_yticklabels(labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr.values[i, j]
            color = "white" if abs(value) > 0.65 else "#0F172A"
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", color=color, fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlação entre rubricas\n", loc="left", pad=24, fontweight="bold")
    fig.text(
        0.08,
        0.89,
        "Mostra se os critérios capturam dimensões semelhantes ou diferentes.",
        fontsize=14,
        color="#475569",
    )
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_stacked_bar(crosstab: pd.DataFrame, title: str, subtitle: str, output_path: Path, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    bottom = np.zeros(len(crosstab))
    x = np.arange(len(crosstab))
    for idx, col in enumerate(crosstab.columns):
        ax.bar(x, crosstab[col].values, bottom=bottom, label=col, color=SLIDE_COLORS[idx % len(SLIDE_COLORS)])
        bottom += crosstab[col].values
    ax.set_xticks(x)
    ax.set_xticklabels([clean_label(v, 24) for v in crosstab.index], rotation=15, ha="right")
    ax.set_ylabel("Quantidade de artigos")
    ax.grid(axis="y")
    set_chart_header(ax, title, subtitle)
    ax.legend(title="Categoria", frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_matrix_heatmap(matrix: pd.DataFrame, title: str, subtitle: str, output_path: Path, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(18, 10))
    values = matrix.values
    im = ax.imshow(values, cmap="YlGnBu")
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_yticks(range(matrix.shape[0]))
    ax.set_xticklabels([clean_label(c, 18) for c in matrix.columns], rotation=30, ha="right")
    ax.set_yticklabels([clean_label(i, 36) for i in matrix.index])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = values[i, j]
            if value:
                ax.text(j, i, str(int(value)), ha="center", va="center", fontsize=11, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    ax.set_title(f"{title}\n", loc="left", pad=24, fontweight="bold")
    fig.text(0.08, 0.89, subtitle, fontsize=14, color="#475569")
    fig.tight_layout()
    save_fig(fig, output_path, dpi)


def plot_overview_cards(df: pd.DataFrame, output_path: Path, dpi: int) -> None:
    total = len(df)
    success = (df["ProcessingStatus"] == "SUCCESS").mean() * 100
    ifrd_mean = pd.to_numeric(df["IFRD"], errors="coerce").mean()
    learning = pd.to_numeric(df["Nota: Aprendizagem"], errors="coerce").mean()
    alignment = pd.to_numeric(df["Nota: Alinhamento"], errors="coerce").mean()
    replication = pd.to_numeric(df["Nota: Replicabilidade"], errors="coerce").mean()
    cards = [
        ("Artigos", f"{total}", "corpus processado"),
        ("Sucesso", f"{success:.0f}%", "processamento"),
        ("IFRD médio", f"{ifrd_mean:.2f}", "indicador final"),
        ("Aprendizagem", f"{learning:.2f}", "média da rubrica"),
        ("Alinhamento", f"{alignment:.2f}", "média da rubrica"),
        ("Replicabilidade", f"{replication:.2f}", "menor média"),
    ]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis("off")
    fig.suptitle("Resumo executivo do corpus", x=0.05, y=0.95, ha="left", fontsize=26, fontweight="bold")
    fig.text(
        0.05,
        0.89,
        "Visão inicial para abrir os resultados da apresentação.",
        fontsize=15,
        color="#475569",
    )
    positions = [(0.05, 0.55), (0.36, 0.55), (0.67, 0.55), (0.05, 0.22), (0.36, 0.22), (0.67, 0.22)]
    for idx, ((label, value, note), (x, y)) in enumerate(zip(cards, positions)):
        rect = plt.Rectangle((x, y), 0.26, 0.23, transform=fig.transFigure, color="#F8FAFC", ec="#CBD5E1", lw=1.5)
        fig.patches.append(rect)
        fig.text(x + 0.025, y + 0.165, label, fontsize=15, color="#475569", fontweight="bold")
        fig.text(x + 0.025, y + 0.075, value, fontsize=34, color=SLIDE_COLORS[idx], fontweight="bold")
        fig.text(x + 0.025, y + 0.032, note, fontsize=13, color="#64748B")
    save_fig(fig, output_path, dpi)


def build_tables(df: pd.DataFrame, synthesis: pd.DataFrame | None, dirs: dict[str, Path], top_n: int) -> dict[str, pd.DataFrame]:
    df = df.copy()
    df["Citações Num"] = normalize_count_column(df, "Citações")
    for col in ["IFRD", *RUBRIC_COLUMNS.keys()]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    tables: dict[str, pd.DataFrame] = {}
    tables["resumo_geral"] = pd.DataFrame(
        [
            ["Total de artigos", len(df)],
            ["Artigos processados com sucesso", int((df["ProcessingStatus"] == "SUCCESS").sum())],
            ["IFRD médio", round(df["IFRD"].mean(), 2)],
            ["IFRD mínimo", round(df["IFRD"].min(), 2)],
            ["IFRD máximo", round(df["IFRD"].max(), 2)],
            ["Média de aprendizagem", round(df["Nota: Aprendizagem"].mean(), 2)],
            ["Média de alinhamento", round(df["Nota: Alinhamento"].mean(), 2)],
            ["Média de replicabilidade", round(df["Nota: Replicabilidade"].mean(), 2)],
        ],
        columns=["Indicador", "Valor"],
    )

    article_cols = [
        "Aluno",
        "Título",
        "Tema",
        "Ano Publicação",
        "Citações",
        "Tipo Veículo",
        "Tipo Estudo",
        "Natureza Pesquisa",
        "Natureza Dados",
        "Nota: Aprendizagem",
        "Nota: Replicabilidade",
        "IFRD",
        "Classificação IFRD",
    ]
    tables["artigos_resumo"] = df[article_cols].sort_values("IFRD", ascending=False)
    tables["ranking_ifrd_top_10"] = tables["artigos_resumo"].head(10)
    tables["ranking_ifrd_bottom_10"] = tables["artigos_resumo"].tail(10).sort_values("IFRD")

    tables["rubricas_estatisticas"] = (
        df[list(RUBRIC_COLUMNS)]
        .agg(["mean", "median", "std", "min", "max"])
        .T.rename(index=RUBRIC_COLUMNS)
        .reset_index(names="Rubrica")
        .round(2)
    )

    def grouped_stats(group_col: str, name: str) -> None:
        tables[name] = (
            df.groupby(group_col, dropna=False)
            .agg(
                quantidade=("Título", "count"),
                ifrd_medio=("IFRD", "mean"),
                aprendizagem_media=("Nota: Aprendizagem", "mean"),
                alinhamento_medio=("Nota: Alinhamento", "mean"),
                replicabilidade_media=("Nota: Replicabilidade", "mean"),
                citacoes_mediana=("Citações Num", "median"),
            )
            .sort_values(["quantidade", "ifrd_medio"], ascending=[False, False])
            .round(2)
            .reset_index()
        )

    grouped_stats("Tipo Estudo", "por_tipo_estudo")
    grouped_stats("Natureza Pesquisa", "por_natureza_pesquisa")
    grouped_stats("Natureza Dados", "por_natureza_dados")
    grouped_stats("Tipo Veículo", "por_tipo_veiculo")
    grouped_stats("Disponibilidade Dados/Código", "por_disponibilidade_dados")

    topic_counts = Counter(split_multivalue(df["Tópicos Específicos"]))
    unit_counts = Counter(split_multivalue(df["Unidades Plano"]))
    method_counts = Counter(split_multivalue(df["Métodos Estatísticos"]))
    metric_counts = Counter(split_multivalue(df["Métricas Software"]))
    artifact_counts = Counter(split_multivalue(df["Artefatos Compartilhados"]))

    tables["cobertura_topicos_ementa"] = pd.DataFrame(topic_counts.most_common(), columns=["Tópico", "Quantidade"])
    tables["cobertura_unidades"] = pd.DataFrame(unit_counts.most_common(), columns=["Unidade", "Quantidade"])
    tables["metodos_estatisticos_top"] = pd.DataFrame(method_counts.most_common(top_n), columns=["Método", "Quantidade"])
    tables["metricas_software_top"] = pd.DataFrame(metric_counts.most_common(top_n), columns=["Métrica", "Quantidade"])
    tables["artefatos_compartilhados"] = pd.DataFrame(artifact_counts.most_common(), columns=["Artefato", "Quantidade"])

    tables["matriz_tipo_estudo_natureza_dados"] = pd.crosstab(df["Tipo Estudo"], df["Natureza Dados"]).reset_index()
    tables["matriz_tipo_estudo_classificacao_ifrd"] = pd.crosstab(
        df["Tipo Estudo"], df["Classificação IFRD"]
    ).reset_index()

    top_topics = tables["cobertura_topicos_ementa"]["Tópico"].head(10).tolist()
    rows = []
    for _, row in df.iterrows():
        article_topics = set(str(row.get("Tópicos Específicos", "")).split("\n"))
        for topic in top_topics:
            if topic in article_topics:
                rows.append({"Tipo Estudo": row["Tipo Estudo"], "Tópico": topic})
    tables["matriz_topicos_tipo_estudo"] = pd.crosstab(
        pd.DataFrame(rows)["Tópico"],
        pd.DataFrame(rows)["Tipo Estudo"],
    ).reset_index() if rows else pd.DataFrame()

    tables["correlacao_rubricas"] = (
        df[list(RUBRIC_COLUMNS)]
        .rename(columns=RUBRIC_COLUMNS)
        .corr()
        .round(3)
        .reset_index(names="Rubrica")
    )

    objective_cols = [
        "Aluno",
        "Título",
        "Questão de Pesquisa",
        "Metodologia",
        "3 Principais Descobertas",
        "Principal Limitação",
        "IFRD",
    ]
    tables["questoes_objetivos_artigos"] = df[objective_cols].sort_values("IFRD", ascending=False)

    if synthesis is not None and not synthesis.empty:
        tables["sintese_tematica"] = synthesis
        relationship_rows = synthesis[synthesis["Seção"].astype(str).str.contains("Relação", na=False)]
        if not relationship_rows.empty:
            tables["relacoes_tematicas_contagem"] = (
                relationship_rows["Tipo/Label"].fillna("N/A").value_counts().rename_axis("Relação").reset_index(name="Quantidade")
            )

    for name, table in tables.items():
        save_table(table, name, dirs)

    return tables


def build_charts(df: pd.DataFrame, tables: dict[str, pd.DataFrame], dirs: dict[str, Path], dpi: int, top_n: int) -> None:
    charts = dirs["charts"]
    df = df.copy()
    for col in ["IFRD", *RUBRIC_COLUMNS.keys()]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    plot_overview_cards(df, charts / "01_resumo_executivo.png", dpi)

    plot_vertical_bar(
        df["Classificação IFRD"].fillna("N/A").value_counts(),
        "Classificação dos artigos pelo IFRD",
        "Distribuição dos artigos nas faixas do indicador final.",
        charts / "02_classificacao_ifrd.png",
        dpi,
    )

    plot_histogram(df, charts / "03_distribuicao_ifrd.png", dpi)

    rubric_means = df[list(RUBRIC_COLUMNS)].mean().rename(index=RUBRIC_COLUMNS).sort_values()
    plot_horizontal_bar(
        rubric_means,
        "Médias das rubricas",
        "O contraste entre aprendizagem/alinhamento e replicabilidade é o principal achado.",
        charts / "04_medias_rubricas_barras.png",
        dpi,
        xlabel="Média na escala 1-5",
        color="#10B981",
        value_fmt="{:.2f}",
    )

    plot_radar(df[list(RUBRIC_COLUMNS)].mean().rename(index=RUBRIC_COLUMNS), charts / "05_medias_rubricas_radar.png", dpi)

    plot_horizontal_bar(
        df["Tipo Estudo"].fillna("N/A").value_counts().sort_values(),
        "Artigos por tipo de estudo",
        "Caracterização metodológica do corpus.",
        charts / "06_tipo_estudo.png",
        dpi,
        color="#2563EB",
    )

    plot_horizontal_bar(
        df["Tipo Veículo"].fillna("N/A").value_counts().sort_values(),
        "Artigos por tipo de veículo",
        "Distribuição entre revistas, conferências, preprints e outros veículos.",
        charts / "07_tipo_veiculo.png",
        dpi,
        color="#8B5CF6",
    )

    plot_donut(
        df["Natureza Pesquisa"].fillna("N/A").value_counts(),
        "Natureza da pesquisa",
        "Mostra o peso de estudos práticos, teóricos e híbridos.",
        charts / "08_natureza_pesquisa.png",
        dpi,
    )

    plot_donut(
        df["Natureza Dados"].fillna("N/A").value_counts(),
        "Natureza dos dados",
        "Mostra o equilíbrio entre dados quantitativos, qualitativos e mistos.",
        charts / "09_natureza_dados.png",
        dpi,
    )

    plot_horizontal_bar(
        df["Disponibilidade Dados/Código"].fillna("N/A").value_counts().sort_values(),
        "Disponibilidade de dados e código",
        "Base para a discussão de replicabilidade.",
        charts / "10_disponibilidade_dados_codigo.png",
        dpi,
        color="#EF4444",
    )

    topicos = tables["cobertura_topicos_ementa"].head(top_n).set_index("Tópico")["Quantidade"].sort_values()
    plot_horizontal_bar(
        topicos,
        "Cobertura dos tópicos da ementa",
        "Tópicos mais frequentes nos artigos analisados.",
        charts / "11_topicos_ementa.png",
        dpi,
        color="#F59E0B",
    )

    unidades = tables["cobertura_unidades"].set_index("Unidade")["Quantidade"].sort_values()
    plot_horizontal_bar(
        unidades,
        "Cobertura das unidades do plano",
        "Quantidade de artigos relacionados a cada unidade.",
        charts / "12_unidades_plano.png",
        dpi,
        color="#06B6D4",
    )

    crosstab = pd.crosstab(df["Tipo Estudo"], df["Natureza Dados"])
    crosstab = crosstab.loc[crosstab.sum(axis=1).sort_values(ascending=False).index]
    plot_stacked_bar(
        crosstab,
        "Tipo de estudo por natureza dos dados",
        "Cruza desenho metodológico com tipo de dado analisado.",
        charts / "13_tipo_estudo_natureza_dados.png",
        dpi,
    )

    plot_boxplot(df, charts / "14_boxplot_ifrd_tipo_estudo.png", dpi)
    plot_scatter_citations(df, charts / "15_citacoes_vs_ifrd.png", dpi)
    plot_correlation_heatmap(df, charts / "16_correlacao_rubricas.png", dpi)

    if "matriz_topicos_tipo_estudo" in tables and not tables["matriz_topicos_tipo_estudo"].empty:
        matrix = tables["matriz_topicos_tipo_estudo"].set_index("Tópico")
        plot_matrix_heatmap(
            matrix,
            "Tópicos da ementa por tipo de estudo",
            "Matriz para discutir sobreposição temática e cobertura metodológica.",
            charts / "17_topicos_por_tipo_estudo.png",
            dpi,
        )

    if "metodos_estatisticos_top" in tables and not tables["metodos_estatisticos_top"].empty:
        metodos = tables["metodos_estatisticos_top"].set_index("Método")["Quantidade"].sort_values()
        plot_horizontal_bar(
            metodos,
            "Métodos estatísticos mais citados",
            "Extraídos da classificação e dos resumos estruturados.",
            charts / "18_metodos_estatisticos.png",
            dpi,
            color="#64748B",
        )

    if "metricas_software_top" in tables and not tables["metricas_software_top"].empty:
        metricas = tables["metricas_software_top"].set_index("Métrica")["Quantidade"].sort_values()
        plot_horizontal_bar(
            metricas,
            "Métricas de software mais citadas",
            "Mostra quais medidas aparecem com maior frequência no corpus.",
            charts / "19_metricas_software.png",
            dpi,
            color="#84CC16",
        )

    year_counts = df["Ano Publicação"].fillna("N/A").astype(str).value_counts()
    year_counts = year_counts.drop(labels=["N/A", "nan"], errors="ignore")
    if not year_counts.empty:
        year_counts.index = year_counts.index.str.replace(".0", "", regex=False)
        year_counts = year_counts.sort_index()
        plot_vertical_bar(
            year_counts,
            "Artigos por ano de publicação",
            "Distribuição temporal dos artigos com ano identificado.",
            charts / "20_artigos_por_ano.png",
            dpi,
        )

    top_ifrd = df.nlargest(10, "IFRD").set_index("Título")["IFRD"].sort_values()
    plot_horizontal_bar(
        top_ifrd,
        "Top 10 artigos por IFRD",
        "Ranking dos artigos com maior aderência e qualidade segundo o indicador.",
        charts / "21_top10_ifrd.png",
        dpi,
        xlabel="IFRD",
        color="#10B981",
        value_fmt="{:.2f}",
    )

    by_study = (
        df.groupby("Tipo Estudo")[["Nota: Aprendizagem", "Nota: Replicabilidade"]]
        .mean()
        .sort_values("Nota: Aprendizagem", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(16, 9))
    x = np.arange(len(by_study))
    width = 0.38
    ax.bar(x - width / 2, by_study["Nota: Aprendizagem"], width, label="Aprendizagem", color="#10B981")
    ax.bar(x + width / 2, by_study["Nota: Replicabilidade"], width, label="Replicabilidade", color="#EF4444")
    ax.set_xticks(x)
    ax.set_xticklabels([clean_label(v, 24) for v in by_study.index], rotation=15, ha="right")
    ax.set_ylim(0, 5.3)
    ax.grid(axis="y")
    ax.set_ylabel("Média na escala 1-5")
    set_chart_header(
        ax,
        "Aprendizagem versus replicabilidade por tipo de estudo",
        "Mostra se o valor didático vem acompanhado de condições de reprodução.",
    )
    ax.legend(frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_fig(fig, charts / "22_aprendizagem_vs_replicabilidade.png", dpi)


def write_report(df: pd.DataFrame, tables: dict[str, pd.DataFrame], dirs: dict[str, Path]) -> None:
    rubric_means = df[list(RUBRIC_COLUMNS)].apply(pd.to_numeric, errors="coerce").mean().rename(index=RUBRIC_COLUMNS)
    report = f"""# Relatório de Tabelas e Gráficos

Este diretório contém tabelas derivadas e gráficos para a apresentação do Trabalho Final - Grupo 2.

## Base analisada

- Arquivo de origem: `classificacao_artigos.xlsx`
- Artigos analisados: **{len(df)}**
- Artigos processados com sucesso: **{int((df["ProcessingStatus"] == "SUCCESS").sum())}**
- IFRD médio: **{pd.to_numeric(df["IFRD"], errors="coerce").mean():.2f}**
- Menor IFRD: **{pd.to_numeric(df["IFRD"], errors="coerce").min():.2f}**
- Maior IFRD: **{pd.to_numeric(df["IFRD"], errors="coerce").max():.2f}**

## Principal leitura para os slides

Os dados indicam forte alinhamento dos artigos com a disciplina e alta contribuição potencial para aprendizagem. O ponto mais fraco é a replicabilidade, especialmente pela baixa disponibilidade de dados, código e artefatos de reprodução.

## Médias das rubricas

{markdown_table(rubric_means.sort_values(ascending=False).round(2).reset_index().rename(columns={"index": "Rubrica", 0: "Média"}))}

## Gráficos sugeridos para apresentação

1. `01_resumo_executivo.png` - abertura dos resultados.
2. `06_tipo_estudo.png` e `08_natureza_pesquisa.png` - caracterização do corpus.
3. `11_topicos_ementa.png` e `12_unidades_plano.png` - aderência ao plano de ensino.
4. `04_medias_rubricas_barras.png` ou `05_medias_rubricas_radar.png` - principais forças e fragilidades.
5. `03_distribuicao_ifrd.png` - distribuição do indicador final.
6. `10_disponibilidade_dados_codigo.png` - discussão de replicabilidade.
7. `15_citacoes_vs_ifrd.png` - relação entre impacto bibliométrico e utilidade didática.
8. `22_aprendizagem_vs_replicabilidade.png` - contraste central para discussão.

## Como usar no slide

- Use os PNGs da pasta `graficos/`; eles foram exportados em formato 16:9 e alta resolução.
- Use as tabelas da pasta `tabelas_md/` quando quiser copiar uma tabela menor para o LaTeX/Beamer.
- Use as tabelas da pasta `tabelas_csv/` para refinar dados no Excel, Power BI ou Python.

## Observação metodológica

O estudo atual sustenta melhor a expressão **contribuição potencial para aprendizagem** do que impacto causal direto. Para afirmar causalidade seria necessário coletar evidência direta de aprendizagem, como pré-teste/pós-teste ou questionário com alunos.
"""
    (dirs["root"] / "RELATORIO_GRAFICOS.md").write_text(report, encoding="utf-8")

    manifest_rows = []
    for folder_name in ["graficos", "tabelas_csv", "tabelas_md"]:
        folder = dirs["root"] / folder_name
        for path in sorted(folder.glob("*")):
            manifest_rows.append({"Tipo": folder_name, "Arquivo": path.name, "Caminho": str(path.relative_to(dirs["root"]))})
    pd.DataFrame(manifest_rows).to_csv(dirs["root"] / "manifesto_arquivos.csv", index=False, encoding="utf-8-sig")


def main() -> int:
    args = parse_args()
    setup_plot_style()

    if not args.input.exists():
        raise SystemExit(f"Arquivo de entrada não encontrado: {args.input}")

    dirs = ensure_dirs(args.output)
    df = pd.read_excel(args.input, sheet_name=MAIN_SHEET)
    try:
        synthesis = pd.read_excel(args.input, sheet_name=SYNTHESIS_SHEET)
    except ValueError:
        synthesis = None

    tables = build_tables(df, synthesis, dirs, args.top_n)
    build_charts(df, tables, dirs, args.dpi, args.top_n)
    write_report(df, tables, dirs)

    print(f"Saida gerada em: {args.output.resolve()}")
    print(f"Graficos: {(args.output / 'graficos').resolve()}")
    print(f"Tabelas CSV: {(args.output / 'tabelas_csv').resolve()}")
    print(f"Tabelas Markdown: {(args.output / 'tabelas_md').resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
