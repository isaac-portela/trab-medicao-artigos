from pydantic import BaseModel, Field
from typing import List

class RubricaNotas(BaseModel):
    qualidade_academica: int = Field(..., description="Nota de 1 a 5 para Qualidade Acadêmica (Rigor, clareza metodológica, reputação da fonte).")
    replicabilidade: int = Field(..., description="Nota de 1 a 5 para Replicabilidade (Presença de dados, método estruturado, scripts ou descrição suficiente).")
    aplicabilidade_pratica: int = Field(..., description="Nota de 1 a 5 para Aplicabilidade Prática (Utilidade para resolver problemas reais de Engenharia de Software).")
    contribuicao_teorica: int = Field(..., description="Nota de 1 a 5 para Contribuição Teórica (Fundamentação científica, modelos propostos, taxonomias).")
    adequacao_aluno: int = Field(..., description="Nota de 1 a 5 para Adequação ao Aluno (Dificuldade de leitura compatível com alunos do 6º período).")
    contribuicao_aprendizagem: int = Field(..., description="Nota de 1 a 5 para Contribuição para Aprendizagem (Quanto ajuda a entender medição, análise estatística ou experimentação).")
    alinhamento_plano: int = Field(..., description="Nota de 1 a 5 para Alinhamento ao Plano de Ensino (Relação com os tópicos de Medição, Análise e Experimentação).")

class JustificativaRubrica(BaseModel):
    qualidade_academica: str = Field(..., description="Justificativa sucinta para a nota de Qualidade Acadêmica.")
    replicabilidade: str = Field(..., description="Justificativa sucinta para a nota de Replicabilidade.")
    aplicabilidade_pratica: str = Field(..., description="Justificativa sucinta para a nota de Aplicabilidade Prática.")
    contribuicao_teorica: str = Field(..., description="Justificativa sucinta para a nota de Contribuição Teórica.")
    adequacao_aluno: str = Field(..., description="Justificativa sucinta para a nota de Adequação ao Aluno.")
    contribuicao_aprendizagem: str = Field(..., description="Justificativa sucinta para a nota de Contribuição para Aprendizagem.")
    alinhamento_plano: str = Field(..., description="Justificativa sucinta para a nota de Alinhamento ao Plano de Ensino.")

class ArtigoClassificado(BaseModel):
    resumo_pt: str = Field(..., description="Resumo curto e estruturado em português brasileiro (máximo 150 palavras).")
    tema_principal: str = Field(..., description="Tema central do artigo (ex: Métricas de Qualidade, Produtividade, DORA, Experimentação, etc.).")
    ano_publicacao: int = Field(..., description="Ano em que o artigo foi publicado (ex: 2023). Se não encontrado, estimar ou usar do info.md.")
    editora_entidade: str = Field(..., description="Editora ou entidade publicadora (ACM, IEEE, Elsevier, Springer, MDPI, arXiv, SBC, etc.).")
    tipo_veiculo: str = Field(..., description="Tipo do veículo de publicação: Revista (Journal), Conferência (Conference), Repositório (arXiv/Preprint), Outro.")
    tipo_estudo_detalhado: str = Field(..., description="Tipo do estudo: Experimento Controlado, Quase-experimento, Estudo de Caso, Survey, Revisão Sistemática, Proposta Conceitual, Outro.")
    natureza_pesquisa: str = Field(..., description="Natureza: Prática (Empírica), Teórica ou Híbrida.")
    natureza_dados: str = Field(..., description="Natureza dos dados analisados: Quantitativa, Qualitativa ou Mista.")
    tamanho_amostra: str = Field(..., description="Descrição resumida do tamanho da amostra (ex: '34 programadores', '125 repositórios GitHub', 'N/A').")
    metodos_estatisticos: List[str] = Field(..., description="Lista de métodos e testes estatísticos usados no artigo (ex: Teste Wilcoxon, Regressão Linear, ANOVA, Estatística Descritiva, nenhum).")
    metricas_software: List[str] = Field(..., description="Lista das métricas de engenharia de software investigadas no artigo (ex: Complexidade Ciclomática, DORA, Story Points, LOC, etc.).")
    
    # Reprodutibilidade
    disponibilidade_dados_codigo: str = Field(..., description="Classificação: Totalmente Disponível, Parcialmente Disponível, Não Disponível.")
    link_pacote_replicacao: str = Field(..., description="Link de repositório de replicação (ex: GitHub, Zenodo) se citado no texto. Se não houver, preencher com 'N/A'.")
    elementos_compartilhados: List[str] = Field(..., description="Elementos compartilhados: Código Fonte, Dataset, Scripts R/Python, Questionários, Nenhum.")
    
    # Conteúdo Científico
    tres_principais_descobertas: List[str] = Field(..., description="Três principais descobertas ou contribuições do estudo em português.")
    principal_limitacao: str = Field(..., description="A principal limitação ou fraqueza indicada pelos autores no artigo (em português).")
    ameacas_validade: List[str] = Field(..., description="Lista de ameaças à validade discutidas (ex: Validade Externa (amostra pequena), Validade de Conclusão, etc.).")
    
    # Alinhamento
    unidades_relacionadas: List[str] = Field(..., description="Lista de Unidades do plano de ensino relacionadas: 'Unidade 1', 'Unidade 2' e/ou 'Unidade 3'.")
    topicos_especificos_ementa: List[str] = Field(..., description="Lista de tópicos específicos do plano de ensino abordados no artigo (ex: Métricas de processo, Testes de hipótese, Planejamento de experimento).")
    conceito_especifico_ilustrado: str = Field(..., description="Parágrafo curto explicando como o artigo ilustra esses conceitos da ementa de forma prática.")
    
    # Avaliação
    notas: RubricaNotas
    justificativas: JustificativaRubrica
