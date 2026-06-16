import logging
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Callable
from .config import ARTIGOS_DIR, OUTPUT_EXCEL
from .pdf_extractor import PDFExtractor
from .gemini_classifier import GeminiClassifier
from .excel_exporter import ExcelExporter

logger = logging.getLogger(__name__)

class ClassificationPipeline:
    """Orchestrator class that runs the full pipeline to scan, extract, classify and export articles."""

    def __init__(self, api_key: str = None, delay_seconds: float = 4.0):
        self.classifier = GeminiClassifier(api_key=api_key)
        self.delay_seconds = delay_seconds

    def parse_info_md(self, info_path: Path) -> Dict[str, str]:
        """Parses title, student, group, and link metadata from an info.md file."""
        metadata = {}
        try:
            content = info_path.read_text(encoding="utf-8")
            
            # Extract title (first H1 line)
            title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
            if title_match:
                metadata["title"] = title_match.group(1).strip()
            
            # Extract bullet points
            aluno_match = re.search(r"-\s*Aluno:\s*(.*)$", content, re.MULTILINE | re.IGNORECASE)
            if aluno_match:
                metadata["student"] = aluno_match.group(1).strip()
                
            grupo_match = re.search(r"-\s*Grupo:\s*(.*)$", content, re.MULTILINE | re.IGNORECASE)
            if grupo_match:
                metadata["group"] = grupo_match.group(1).strip()
                
            link_match = re.search(r"-\s*Link original:\s*(.*)$", content, re.MULTILINE | re.IGNORECASE)
            if link_match:
                metadata["link"] = link_match.group(1).strip()
        except Exception as e:
            logger.error(f"Error parsing metadata from {info_path}: {e}")
            
        return metadata

    def run(self, dry_run: bool = False, progress_callback: Callable[[int, int, str], None] = None) -> Path:
        """
        Runs the full classification pipeline.
        If dry_run is True, it runs for only 1 article as a test.
        """
        logger.info(f"Scanning directory: {ARTIGOS_DIR}")
        info_files = list(ARTIGOS_DIR.glob("**/info.md"))
        total_articles = len(info_files)
        logger.info(f"Found {total_articles} articles to process.")

        if dry_run:
            logger.info("Dry run enabled. Processing only 1 article.")
            info_files = info_files[:1]
            total_articles = 1

        results = []

        for idx, info_file in enumerate(info_files, 1):
            folder = info_file.parent
            pdf_path = folder / "artigo.pdf"
            has_pdf = pdf_path.exists()
            
            # Parse metadata
            meta = self.parse_info_md(info_file)
            title = meta.get("title", folder.name)
            student = meta.get("student", "Desconhecido")
            group = meta.get("group", folder.parent.name) # Use folder structure as fallback for group
            link = meta.get("link", "N/A")

            # Report progress
            if progress_callback:
                progress_callback(idx, total_articles, title)
            else:
                logger.info(f"[{idx}/{total_articles}] Processing: {title}")

            # Extract PDF text if available
            pdf_text = ""
            if has_pdf:
                pdf_text = PDFExtractor.extract_text(pdf_path)

            try:
                # Classify using LLM
                classification = self.classifier.classify_article(
                    title=title,
                    student=student,
                    group=group,
                    pdf_text=pdf_text
                )
                
                # Consolidate dictionary to match Excel schema
                article_record = {
                    "Grupo": group,
                    "Aluno": student,
                    "Título": title,
                    "Tem PDF": "Sim" if has_pdf else "Não",
                    "Ano Publicação": classification.ano_publicacao,
                    "Editora": classification.editora_entidade,
                    "Tipo Veículo": classification.tipo_veiculo,
                    "Tipo Estudo": classification.tipo_estudo_detalhado,
                    "Natureza Pesquisa": classification.natureza_pesquisa,
                    "Natureza Dados": classification.natureza_dados,
                    "Tamanho Amostra": classification.tamanho_amostra,
                    
                    # Rubric Notes
                    "Nota: Qualidade": classification.notas.qualidade_academica,
                    "Nota: Replicabilidade": classification.notas.replicabilidade,
                    "Nota: Aplicabilidade": classification.notas.aplicabilidade_pratica,
                    "Nota: Contribuição Teórica": classification.notas.contribuicao_teorica,
                    "Nota: Adequação": classification.notas.adequacao_aluno,
                    "Nota: Aprendizagem": classification.notas.contribuicao_aprendizagem,
                    "Nota: Alinhamento": classification.notas.alinhamento_plano,
                    
                    # Descriptive lists / fields
                    "Métodos Estatísticos": ", ".join(classification.metodos_estatisticos),
                    "Métricas Software": ", ".join(classification.metricas_software),
                    "Replicabilidade (Dados/Código)": classification.disponibilidade_dados_codigo,
                    "Link Replicação": classification.link_pacote_replicacao,
                    "Elementos Compartilhados": ", ".join(classification.elementos_compartilhados),
                    "3 Principais Descobertas": "\n".join(f"- {d}" for d in classification.tres_principais_descobertas),
                    "Principal Limitação": classification.principal_limitacao,
                    "Ameaças à Validade": ", ".join(classification.ameacas_validade),
                    "Unidades Plano": ", ".join(classification.unidades_relacionadas),
                    "Tópicos Específicos": ", ".join(classification.topicos_especificos_ementa),
                    "Conceito Ilustrado": classification.conceito_especifico_ilustrado,
                    
                    # Texts
                    "Resumo PT": classification.resumo_pt,
                    "Justificativas": (
                        f"Qualidade: {classification.justificativas.qualidade_academica}\n"
                        f"Replicabilidade: {classification.justificativas.replicabilidade}\n"
                        f"Aplicabilidade: {classification.justificativas.aplicabilidade_pratica}\n"
                        f"Teórica: {classification.justificativas.contribuicao_teorica}\n"
                        f"Adequação: {classification.justificativas.adequacao_aluno}\n"
                        f"Aprendizagem: {classification.justificativas.contribuicao_aprendizagem}\n"
                        f"Alinhamento: {classification.justificativas.alinhamento_plano}"
                    )
                }
                
                results.append(article_record)
            except Exception as e:
                logger.error(f"Failed to process '{title}' due to API or parsing errors: {e}")
                # Append a fallback record so the article is not lost in the Excel list
                fallback_record = {
                    "Grupo": group,
                    "Aluno": student,
                    "Título": title,
                    "Tem PDF": "Sim" if has_pdf else "Não",
                    "Ano Publicação": 0,
                    "Editora": "Erro de classificação",
                    "Tipo Veículo": "Erro",
                    "Tipo Estudo": "Erro",
                    "Natureza Pesquisa": "Erro",
                    "Natureza Dados": "Erro",
                    "Tamanho Amostra": "N/A",
                    "Nota: Qualidade": 1,
                    "Nota: Replicabilidade": 1,
                    "Nota: Aplicabilidade": 1,
                    "Nota: Contribuição Teórica": 1,
                    "Nota: Adequação": 1,
                    "Nota: Aprendizagem": 1,
                    "Nota: Alinhamento": 1,
                    "Métodos Estatísticos": "",
                    "Métricas Software": "",
                    "Replicabilidade (Dados/Código)": "Erro",
                    "Link Replicação": "N/A",
                    "Elementos Compartilhados": "",
                    "3 Principais Descobertas": "",
                    "Principal Limitação": "Erro no processamento da API do Gemini",
                    "Ameaças à Validade": "",
                    "Unidades Plano": "",
                    "Tópicos Específicos": "",
                    "Conceito Ilustrado": "Falha na análise",
                    "Resumo PT": f"Falha na API: {str(e)}",
                    "Justificativas": "Não gerado devido a erros."
                }
                results.append(fallback_record)

            # Delay to avoid hitting rate limits on free-tier keys
            if idx < total_articles and self.delay_seconds > 0:
                time.sleep(self.delay_seconds)

        # Export raw results to stylized Excel sheet
        logger.info(f"Exporting data to: {OUTPUT_EXCEL}")
        ExcelExporter.export(results, OUTPUT_EXCEL)
        logger.info("Excel file generated successfully!")
        
        return OUTPUT_EXCEL
