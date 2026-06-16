import json
import logging
from google import genai
from google.genai import types
from .config import GEMINI_MODEL, TOPICOS_EMENTA, UNIDADES
from .models import ArtigoClassificado

logger = logging.getLogger(__name__)

class GeminiClassifier:
    """Class responsible for communicating with the Gemini API to classify articles."""

    def __init__(self, api_key: str = None):
        # Initializes the Google GenAI client.
        # If api_key is None, GenAI SDK will look for GEMINI_API_KEY environment variable.
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()

    def classify_article(self, title: str, student: str, group: str, pdf_text: str = "") -> ArtigoClassificado:
        """
        Classifies an article using the Gemini API based on its title, student/group metadata,
        and extracted PDF text (if available).
        """
        # Map syllabus units and topics to help the LLM contextualize
        syllabus_context = f"""
        UNIDADES DA DISCIPLINA:
        {json.dumps(UNIDADES, indent=2, ensure_ascii=False)}

        TÓPICOS ESPECÍFICOS DA EMENTA DISPONÍVEIS PARA MAPEAMENTO:
        {json.dumps(TOPICOS_EMENTA, indent=2, ensure_ascii=False)}
        """

        prompt = f"""
        Você é um PhD em Engenharia de Software e um revisor acadêmico rigoroso da disciplina de 'Medição e Experimentação em Engenharia de Software'.
        Sua tarefa é analisar o artigo científico a seguir (metadados e conteúdo extraído) e gerar uma classificação profunda em formato estruturado.

        {syllabus_context}

        DADOS DO ARTIGO A SER AVALIADO:
        - Título do Artigo: {title}
        - Apresentador (Aluno): {student}
        - Turma/Grupo: {group}
        - Texto do Artigo (extraído do PDF):
        --- INÍCIO DO TEXTO ---
        {pdf_text if pdf_text else "[PDF COMPLETO NÃO DISPONÍVEL - AVALIE APENAS PELOS METADADOS/TÍTULO]"}
        --- FIM DO TEXTO ---

        INSTRUÇÕES IMPORTANTES PARA AVALIAÇÃO:
        1. Resumo em Português: Escreva um resumo acadêmico em português brasileiro, destacando a motivação, o método e o resultado (máximo 150 palavras).
        2. Tópicos da Ementa: Escolha exatamente os tópicos da lista 'TÓPICOS ESPECÍFICOS DA EMENTA' que são investigados ou ilustrados no artigo.
        3. Métodos Estatísticos: Identifique quais técnicas estatísticas foram empregadas (ex: Teste t, Teste Wilcoxon, Regressão Linear, ANOVA, Estatística Descritiva). Se nenhuma técnica estatística foi utilizada, indique 'nenhuma'.
        4. Métricas de Software: Identifique quais métricas foram discutidas ou analisadas (ex: complexidade ciclomática, linhas de código, DORA, SPACE, métricas de coesão, etc.).
        5. Reprodutibilidade: Procure no texto por menções a pacotes de replicação (GitHub, Zenodo, etc.) e identifique os artefatos compartilhados.
        6. Rubricas de Nota (1 a 5):
           - Qualidade Acadêmica: Rigor metodológico e relevância da fonte.
           - Replicabilidade: Presença de material de apoio ou descrição detalhada do procedimento experimental.
           - Aplicabilidade Prática: Utilidade imediata na indústria ou resolução de problemas reais de engenharia.
           - Contribuição Teórica: Proposição de novos conceitos, taxonomias ou modelos científicos.
           - Adequação ao Aluno: Se o artigo tem complexidade adequada para alunos do 6º período.
           - Contribuição para Aprendizagem: Relevância do conteúdo específico para o aprendizado prático de medição e experimentação.
           - Alinhamento ao Plano de Ensino: Quão bem se conecta com as Unidades 1, 2 e 3 da disciplina.
        """

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ArtigoClassificado,
                    temperature=0.1  # Low temperature for deterministic/objective evaluation
                )
            )

            # Validate and parse structured response using Pydantic
            raw_text = response.text
            if not raw_text:
                raise ValueError("Empty response text from Gemini API")

            # Parse JSON using model validation
            classification = ArtigoClassificado.model_validate_json(raw_text)
            return classification

        except Exception as e:
            logger.error(f"Error classifying article '{title}': {e}", exc_info=True)
            raise e
