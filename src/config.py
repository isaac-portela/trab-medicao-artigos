from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIGOS_DIR = BASE_DIR / "artigos"
OUTPUT_EXCEL = BASE_DIR / "classificacao_artigos.xlsx"
CACHE_PATH = BASE_DIR / ".citation_cache.json"
CHECKPOINTS_DIR = BASE_DIR / ".adk_checkpoints"

GEMINI_MODEL = "gemini-2.0-flash"

MAX_DEPTH = 3
MAX_PDF_CHARS = 80_000
DEFAULT_DELAY = 4.0
MIN_DELAY = 1.0
MAX_DELAY = 60.0
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2
CACHE_TTL_DAYS = 7

UNIDADES = {"Unidade 1", "Unidade 2", "Unidade 3"}

TOPICOS_EMENTA = [
    "Métricas de produto",
    "Métricas de processo",
    "Métricas de projeto",
    "Processos e técnicas de medição",
    "Identificação, organização e validação de métricas de software",
    "Distribuições de probabilidade",
    "Testes de hipótese",
    "Análise multivariada",
    "Estratégias de experimentação",
    "Processo de experimentação",
    "Planejamento de experimento",
    "Execução de experimento",
    "Análise de resultados de experimentos",
    "Apresentação de resultados experimentais",
]

IFRD_WEIGHTS = {
    "qualidade_academica": 0.25,
    "alinhamento_plano": 0.20,
    "contribuicao_aprendizagem": 0.20,
    "replicabilidade": 0.15,
    "aplicabilidade_pratica": 0.10,
    "adequacao_aluno": 0.10,
}
