import argparse
import os
import sys
import logging
from pathlib import Path
from tqdm import tqdm

# Adjust path to import from the src directory
sys.path.append(str(Path(__file__).resolve().parent))

from dotenv import load_dotenv
from src.pipeline import ClassificationPipeline
from src.config import OUTPUT_EXCEL

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("run_pipeline")

def main():
    # Load environment variables from .env file (checking multiple common directories)
    dotenv_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path(__file__).resolve().parent / "src" / ".env"
    ]
    loaded = False
    for path in dotenv_paths:
        if path.exists():
            load_dotenv(dotenv_path=path)
            loaded = True
            break
    if not loaded:
        load_dotenv()
    
    parser = argparse.ArgumentParser(description="Pipeline de Classificação de Artigos usando Gemini API")
    parser.add_argument("--dry-run", action="store_true", help="Executa o pipeline para apenas 1 artigo como teste seco.")
    parser.add_argument("--delay", type=float, default=4.0, help="Tempo de espera (em segundos) entre as chamadas da API (evita limites de requisição).")
    args = parser.parse_args()

    # Validate API key presence
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        logger.error(
            "Variável de ambiente GEMINI_API_KEY não encontrada!\n"
            "Por favor, configure-a no seu terminal usando:\n"
            "  Windows (cmd): set GEMINI_API_KEY=sua_chave\n"
            "  Windows (PowerShell): $env:GEMINI_API_KEY=\"sua_chave\"\n"
            "  Linux/macOS: export GEMINI_API_KEY=\"sua_chave\""
        )
        sys.exit(1)

    logger.info("Iniciando pipeline de classificação...")
    if args.dry_run:
        logger.info("Executando no MODO DRY-RUN (apenas 1 artigo de teste)...")

    # Initialize and execute pipeline
    pipeline = ClassificationPipeline(api_key=api_key, delay_seconds=args.delay)

    # Simple callback for progress updating with tqdm
    pbar = None
    
    def progress_callback(current: int, total: int, article_title: str):
        nonlocal pbar
        if pbar is None:
            pbar = tqdm(total=total, desc="Classificando Artigos", unit="artigo")
        pbar.set_postfix({"Artigo": article_title[:30] + "..." if len(article_title) > 30 else article_title})
        pbar.update(1)

    try:
        output_file = pipeline.run(dry_run=args.dry_run, progress_callback=progress_callback)
        if pbar:
            pbar.close()
        logger.info(f"Pipeline concluído com sucesso! Planilha gerada em: {output_file.resolve()}")
    except Exception as e:
        if pbar:
            pbar.close()
        logger.error(f"Ocorreu um erro catastrófico na execução do pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
