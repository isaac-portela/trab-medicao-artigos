import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIGOS_DIR = BASE_DIR / "artigos"
OUTPUT_EXCEL = BASE_DIR / "classificacao_artigos.xlsx"

# Syllabus Configuration (plano-de-ensino-2026-1.md)
UNIDADES = {
    "Unidade 1": "Medição em Engenharia de Software",
    "Unidade 2": "Análise de Medições de Software",
    "Unidade 3": "Experimentação em Engenharia de Software",
}

TOPICOS_EMENTA = [
    # Unidade 1
    "Métricas de produto",
    "Métricas de processo",
    "Métricas de projeto",
    "Processos e técnicas de medição",
    "Identificação, organização e validação de métricas de software",
    # Unidade 2
    "Distribuições de probabilidade",
    "Testes de hipótese",
    "Análise multivariada",
    # Unidade 3
    "Estratégias de experimentação",
    "Processo de experimentação",
    "Planejamento de experimento",
    "Execução de experimento",
    "Análise de resultados de experimentos",
    "Apresentação de resultados experimentais",
]

# API Configuration
GEMINI_MODEL = "gemini-2.0-flash"
API_KEY = os.environ.get("GEMINI_API_KEY", "")
