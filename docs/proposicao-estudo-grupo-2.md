# Proposição do Estudo - Grupo 2

## Título Proposto

**Impacto da Leitura de Artigos no Aprendizado em Medição e Experimentação em Engenharia de Software: um Estudo Observacional**

## Ideia

O estudo parte da análise dos artigos apresentados pelos alunos da disciplina de Medição e Experimentação em Engenharia de Software. A ideia central é transformar esse conjunto de artigos em um corpus estruturado, permitindo observar padrões de tema, método, qualidade, replicabilidade, alinhamento com a disciplina e contribuição para o aprendizado.

Para isso, foi construído um pipeline multiagente baseado em ADK, no qual agentes especializados executam etapas diferentes da análise:

- **Reader Agent:** extrai e resume as informações essenciais de cada artigo.
- **Classifier Agent:** classifica metadados, tema, tipo de estudo, natureza da pesquisa e relação com o plano de ensino.
- **Critic Agent:** avalia criticamente cada artigo por rubricas de 1 a 5.
- **Synthesizer Agent:** produz uma síntese transversal do conjunto de artigos, identificando relações temáticas, continuidade e complementação.

A proposta não é medir diretamente o aprendizado individual de cada aluno por prova ou questionário, mas estimar a contribuição potencial dos artigos para o aprendizado com base em critérios observáveis: aderência ao plano de ensino, adequação ao nível do aluno, qualidade acadêmica, replicabilidade, aplicabilidade prática e valor didático.

## Escopo

O escopo do estudo compreende os artigos coletados e organizados no projeto, processados pela planilha `classificacao_artigos.xlsx`.

Até o momento, o corpus analisado possui:

- **84 artigos processados com sucesso.**
- **47 variáveis consolidadas na planilha principal.**
- **1 aba de síntese temática**, contendo relações entre artigos e discussão sobre o IFRD.

O estudo considera os seguintes tipos de informação:

- Metadados dos artigos: título, aluno, grupo, link e pasta.
- Características bibliográficas: ano de publicação, editora ou entidade, tipo de veículo e número de citações.
- Características metodológicas: tipo de estudo, natureza da pesquisa, natureza dos dados, tamanho da amostra e métodos estatísticos.
- Relação com a disciplina: unidades do plano de ensino e tópicos específicos da ementa.
- Avaliação crítica: notas e justificativas para qualidade, replicabilidade, aplicabilidade, contribuição teórica, adequação ao aluno, contribuição para aprendizagem e alinhamento ao plano.
- Indicador sintético: IFRD, calculado por média ponderada das rubricas.
- Síntese temática: clusters, sobreposição, continuidade e complementação entre artigos.

Ficam fora do escopo, nesta etapa:

- Aplicação de questionários aos alunos.
- Medição direta de desempenho antes e depois da leitura.
- Reavaliação manual completa de todos os PDFs.
- Validação externa das notas atribuídas pelos agentes.

## Objetivo

### Objetivo Geral

Avaliar, de forma observacional e estruturada, como os artigos apresentados em sala se relacionam com os conteúdos da disciplina e qual é sua contribuição potencial para o aprendizado em Medição e Experimentação em Engenharia de Software.

### Objetivos Específicos

- Consolidar os artigos apresentados em uma base única de análise.
- Classificar os artigos por tema, ano, citações, veículo, tipo de estudo e natureza da pesquisa.
- Avaliar criticamente os artigos por rubricas acadêmicas e pedagógicas.
- Medir a aderência dos artigos ao plano de ensino da disciplina.
- Investigar a replicabilidade dos artigos com base na disponibilidade de dados, código, scripts e protocolos.
- Identificar relações temáticas entre os artigos, como sobreposição, continuidade e complementação.
- Propor e discutir o IFRD como indicador final de aderência e qualidade.
- Gerar visualizações capazes de apoiar a apresentação e a discussão dos resultados.

## Variáveis

As variáveis do estudo foram organizadas em grupos para facilitar a análise.

### Variáveis de Identificação

| Variável | Tipo | Descrição |
| --- | --- | --- |
| Grupo | Categórica | Turma ou grupo de origem do artigo. |
| Aluno | Categórica | Aluno responsável pela apresentação do artigo. |
| Título | Texto | Título do artigo analisado. |
| Link | Texto | Link informado para o artigo, quando disponível. |
| ProcessingStatus | Categórica | Status do processamento no pipeline. |

### Variáveis Bibliográficas

| Variável | Tipo | Descrição |
| --- | --- | --- |
| Ano Publicação | Quantitativa discreta | Ano em que o artigo foi publicado. |
| Citações | Quantitativa discreta | Número de citações recuperado pelo serviço externo. |
| Origem Citações | Categórica | Fonte da informação de citações. |
| Editora/Entidade | Categórica | Editora, conferência, revista ou entidade associada ao artigo. |
| Tipo Veículo | Categórica | Revista, conferência, preprint ou outro. |

### Variáveis Metodológicas

| Variável | Tipo | Descrição |
| --- | --- | --- |
| Tema | Categórica/textual | Tema central identificado no artigo. |
| Tipo Estudo | Categórica | Experimento controlado, estudo de caso, survey, revisão sistemática, proposta conceitual ou outro. |
| Natureza Pesquisa | Categórica | Prática, teórica ou híbrida. |
| Natureza Dados | Categórica | Quantitativa, qualitativa ou mista. |
| Tamanho Amostra | Texto/quantitativa quando possível | Amostra usada no artigo, quando identificada. |
| Métodos Estatísticos | Lista categórica | Técnicas estatísticas declaradas ou inferidas a partir do resumo estruturado. |
| Métricas Software | Lista categórica | Métricas de software mencionadas no artigo. |

### Variáveis Pedagógicas

| Variável | Tipo | Descrição |
| --- | --- | --- |
| Unidades Plano | Lista categórica | Unidades do plano de ensino relacionadas ao artigo. |
| Tópicos Específicos | Lista categórica | Tópicos da ementa relacionados ao artigo. |
| Nota: Adequação | Ordinal | Compatibilidade do artigo com alunos do 6º período. |
| Nota: Aprendizagem | Ordinal | Contribuição potencial do artigo para o aprendizado. |
| Nota: Alinhamento | Ordinal | Aderência do artigo ao plano de ensino. |

### Variáveis de Qualidade e Replicabilidade

| Variável | Tipo | Descrição |
| --- | --- | --- |
| Nota: Qualidade | Ordinal | Rigor, clareza, confiabilidade e validade metodológica. |
| Nota: Replicabilidade | Ordinal | Possibilidade de repetição do estudo por terceiros. |
| Nota: Aplicabilidade | Ordinal | Utilidade prática para problemas reais de engenharia de software. |
| Nota: Contribuição Teórica | Ordinal | Contribuição conceitual, científica ou metodológica. |
| Disponibilidade Dados/Código | Categórica | Totalmente disponível, parcialmente disponível ou não disponível. |
| Artefatos Compartilhados | Lista categórica | Código, dataset, scripts, questionários ou nenhum. |
| Links Replicação | Lista textual | Links identificados para reprodução ou materiais complementares. |

### Variável Sintética

| Variável | Tipo | Descrição |
| --- | --- | --- |
| IFRD | Quantitativa contínua | Índice final calculado por média ponderada das rubricas. |
| Classificação IFRD | Categórica ordinal | Faixa interpretativa do IFRD: fraco, intermediário ou bom artigo. |

## Identificação de Variáveis Dependentes e Independentes

Como o estudo é observacional, as variáveis não são manipuladas experimentalmente. Ainda assim, para fins de análise, é possível organizar as variáveis em explicativas e de resultado.

### Variáveis Dependentes

As variáveis dependentes representam os resultados que o estudo deseja explicar ou discutir:

- **Nota: Aprendizagem:** principal variável associada à contribuição do artigo para o aprendizado.
- **Nota: Alinhamento:** mede a aderência ao plano de ensino.
- **Nota: Adequação:** mede se o artigo é compatível com o nível dos alunos.
- **IFRD:** indicador final de aderência e qualidade.
- **Classificação IFRD:** versão categórica do IFRD.

### Variáveis Independentes

As variáveis independentes são características dos artigos que podem ajudar a explicar diferenças nas variáveis dependentes:

- Tipo de estudo.
- Natureza da pesquisa.
- Natureza dos dados.
- Tipo de veículo.
- Ano de publicação.
- Número de citações.
- Tema.
- Métodos estatísticos utilizados.
- Métricas de software abordadas.
- Disponibilidade de dados ou código.
- Artefatos compartilhados.
- Unidades e tópicos da ementa associados ao artigo.

### Relações Analíticas Possíveis

Algumas perguntas que podem orientar a análise:

- Artigos com maior alinhamento ao plano também possuem maior contribuição para aprendizagem?
- Artigos com dados ou código disponíveis possuem maior nota de replicabilidade?
- Artigos empíricos têm maior aplicabilidade prática que artigos teóricos?
- Revisões sistemáticas tendem a ter maior contribuição teórica ou maior alinhamento com a disciplina?
- Artigos mais recentes apresentam maior aderência aos temas de experimentação e métricas?
- O número de citações se relaciona com a qualidade acadêmica atribuída?
- A replicabilidade é o ponto mais fraco do corpus?

## Caracterização

A caracterização inicial do corpus mostra que todos os 84 artigos foram processados com sucesso pelo pipeline.

### Distribuição por Classificação IFRD

| Classificação | Quantidade |
| --- | ---: |
| Bom Artigo | 55 |
| Intermediário | 26 |
| Fraco | 3 |

O IFRD médio foi **4,09**, com mínimo de **2,20** e máximo de **4,80**. Isso sugere que, de modo geral, o conjunto de artigos possui boa aderência à disciplina e bom potencial didático, embora existam diferenças relevantes entre os critérios.

### Distribuição por Tipo de Veículo

| Tipo de Veículo | Quantidade |
| --- | ---: |
| Revista | 26 |
| Conferência | 23 |
| Outro | 20 |
| Repositório / Preprint | 15 |

### Distribuição por Tipo de Estudo

| Tipo de Estudo | Quantidade |
| --- | ---: |
| Experimento Controlado | 22 |
| Revisão Sistemática | 21 |
| Estudo de Caso | 19 |
| Proposta Conceitual | 12 |
| Survey | 7 |
| Outro | 3 |

### Natureza da Pesquisa

| Natureza | Quantidade |
| --- | ---: |
| Prática / Empírica | 48 |
| Híbrida | 21 |
| Teórica | 15 |

### Natureza dos Dados

| Natureza dos Dados | Quantidade |
| --- | ---: |
| Mista | 33 |
| Quantitativa | 30 |
| Qualitativa | 21 |

### Disponibilidade de Dados e Código

| Disponibilidade | Quantidade |
| --- | ---: |
| Não Disponível | 60 |
| Parcialmente Disponível | 24 |

Nenhum artigo foi classificado como totalmente disponível na base atual. Esse é um ponto importante para discussão, porque a replicabilidade aparece como a dimensão mais fraca do conjunto analisado.

### Médias das Rubricas

| Rubrica | Média |
| --- | ---: |
| Alinhamento ao Plano | 4,90 |
| Contribuição para Aprendizagem | 4,48 |
| Aplicabilidade Prática | 4,29 |
| Qualidade Acadêmica | 4,08 |
| Contribuição Teórica | 3,86 |
| Adequação ao Aluno | 3,75 |
| Replicabilidade | 2,58 |

Esse resultado indica uma tensão relevante: os artigos são, em média, bem alinhados à disciplina e úteis para aprendizagem, mas apresentam baixa replicabilidade.

### Cobertura do Plano de Ensino

| Unidade | Quantidade de Artigos Relacionados |
| --- | ---: |
| Unidade 2 | 84 |
| Unidade 3 | 79 |
| Unidade 1 | 53 |

Os tópicos mais frequentes foram:

| Tópico da Ementa | Quantidade |
| --- | ---: |
| Análise de resultados de experimentos | 73 |
| Métricas de processo | 63 |
| Planejamento de experimento | 60 |
| Apresentação de resultados experimentais | 60 |
| Métricas de produto | 59 |
| Execução de experimento | 59 |
| Identificação, organização e validação de métricas de software | 54 |
| Métricas de projeto | 52 |
| Processos e técnicas de medição | 51 |
| Estratégias de experimentação | 50 |
| Processo de experimentação | 48 |
| Análise multivariada | 39 |
| Testes de hipótese | 37 |
| Distribuições de probabilidade | 22 |

## Visualização

A planilha principal pode ser transformada em um conjunto de tabelas derivadas e gráficos para apoiar a apresentação. A ideia é não mostrar apenas a tabela completa, mas criar visões resumidas por pergunta de análise.

### Tabelas Derivadas Recomendadas

| Tabela | Colunas | Finalidade |
| --- | --- | --- |
| Resumo geral do corpus | Total de artigos, IFRD médio, maior IFRD, menor IFRD, total por status | Abrir a apresentação com uma visão executiva. |
| Artigos por tipo de estudo | Tipo Estudo, quantidade, IFRD médio, aprendizagem média, replicabilidade média | Comparar desenhos metodológicos. |
| Artigos por natureza da pesquisa | Natureza Pesquisa, quantidade, aplicabilidade média, contribuição teórica média | Comparar artigos práticos, teóricos e híbridos. |
| Replicabilidade por disponibilidade | Disponibilidade Dados/Código, quantidade, nota média de replicabilidade | Evidenciar o principal ponto fraco do corpus. |
| Cobertura da ementa | Tópico Específico, quantidade de artigos | Mostrar quais tópicos da disciplina foram mais cobertos. |
| Ranking IFRD | Título, aluno, tipo de estudo, IFRD, classificação | Identificar artigos de maior aderência e qualidade. |
| Rubricas médias | Rubrica, média, desvio padrão | Comparar forças e fragilidades da base. |
| Relações temáticas | Tipo de relação, artigos relacionados, descrição | Mostrar sobreposição, continuidade e complementação entre artigos. |

### Gráficos Recomendados

1. **Gráfico de barras: quantidade de artigos por classificação IFRD**
   - Mostra rapidamente a distribuição entre bom, intermediário e fraco.
   - Serve para defender que a maior parte do corpus tem boa qualidade geral.

2. **Histograma do IFRD**
   - Mostra a concentração dos artigos por faixa de pontuação.
   - Ajuda a explicar se o corpus é homogêneo ou se há muita dispersão.

3. **Radar das médias das rubricas**
   - Eixos: qualidade, replicabilidade, aplicabilidade, contribuição teórica, adequação, aprendizagem e alinhamento.
   - Excelente para mostrar o contraste entre alto alinhamento/aprendizagem e baixa replicabilidade.

4. **Barras horizontais dos tópicos da ementa**
   - Mostra quais tópicos aparecem mais nos artigos.
   - É útil para demonstrar aderência ao plano de ensino.

5. **Barras empilhadas: tipo de estudo por natureza dos dados**
   - Cruza experimento, revisão, estudo de caso, survey etc. com dados quantitativos, qualitativos e mistos.
   - Ajuda a caracterizar a diversidade metodológica do corpus.

6. **Boxplot do IFRD por tipo de estudo**
   - Compara a distribuição do IFRD entre experimentos controlados, revisões sistemáticas, estudos de caso e propostas conceituais.
   - Ajuda a observar se algum tipo de estudo tende a pontuar melhor.

7. **Dispersão: citações versus IFRD**
   - Eixo X: citações.
   - Eixo Y: IFRD.
   - Permite discutir se impacto bibliométrico acompanha ou não a aderência didática.

8. **Heatmap de correlação das rubricas**
   - Cruza notas de qualidade, replicabilidade, aplicabilidade, contribuição teórica, adequação, aprendizagem e alinhamento.
   - Útil para identificar se as rubricas se movem juntas ou capturam dimensões diferentes.

9. **Gráfico de barras: disponibilidade de dados/código**
   - Evidencia que 60 artigos não possuem dados/código disponíveis e 24 possuem disponibilidade parcial.
   - Deve ser usado na discussão sobre replicabilidade.

10. **Rede temática ou matriz artigo-tema**
    - Nós: artigos e tópicos da ementa.
    - Arestas: relação artigo-tópico.
    - Alternativa mais simples: matriz binária com artigos nas linhas e tópicos nas colunas.
    - Boa visualização para mostrar sobreposição temática.

### Ordem Sugerida das Visualizações na Apresentação

1. Visão geral do pipeline ADK.
2. Total de artigos processados e status.
3. Distribuição por tipo de estudo e natureza da pesquisa.
4. Cobertura dos tópicos da ementa.
5. Médias das rubricas em gráfico radar ou barras.
6. Distribuição do IFRD.
7. Replicabilidade e disponibilidade de dados/código.
8. Relações temáticas entre artigos.
9. Discussão das hipóteses H0 e H1.
10. Limitações e próximos passos.

## Discussão

Os resultados iniciais indicam que os artigos analisados possuem forte relação com a disciplina. A média de alinhamento ao plano foi **4,90**, e a média de contribuição para aprendizagem foi **4,48**, sugerindo que a leitura dos artigos tende a apoiar o aprendizado dos conteúdos de Medição e Experimentação em Engenharia de Software.

Por outro lado, a replicabilidade teve média **2,58**, sendo a menor rubrica entre todas. Esse resultado mostra que muitos artigos podem ser bons como material didático, mas não necessariamente oferecem condições completas para reprodução dos estudos. A baixa disponibilidade de dados e código reforça esse ponto: 60 artigos foram classificados como sem disponibilidade e 24 como parcialmente disponíveis.

A partir disso, a hipótese nula e a hipótese alternativa podem ser discutidas com cautela:

- **H0:** a leitura de artigos não impacta o aprendizado, na média.
- **H1:** a leitura dos artigos impacta o aprendizado, na média.

Como o estudo atual não mede diretamente o aprendizado individual antes e depois da leitura, não é adequado afirmar causalidade forte. O que os dados permitem defender é uma evidência observacional de contribuição potencial para o aprendizado, especialmente pelo alto alinhamento ao plano de ensino e pela alta nota média de contribuição para aprendizagem.

Assim, a discussão pode seguir a seguinte linha:

- Os artigos estão bem alinhados à disciplina.
- O conjunto cobre majoritariamente tópicos de experimentação, métricas e análise de resultados.
- A maioria dos artigos tem natureza prática ou híbrida, o que favorece conexão com problemas reais de Engenharia de Software.
- A contribuição didática é alta, mas a replicabilidade é uma limitação importante.
- O IFRD é útil como indicador sintético, mas não substitui análise qualitativa das justificativas e limitações.

## Metodologia de Classificação para Explicar ao Professor

A metodologia adotada pode ser explicada como uma pipeline de análise assistida por IA, com controle estrutural por modelos Pydantic e saída consolidada em planilha.

Fluxo resumido:

1. **Organização dos artigos**
   - Cada artigo foi salvo em uma estrutura padronizada de pastas.
   - Cada pasta contém o PDF do artigo e metadados em `info.md`.

2. **Extração de texto**
   - O PDF é convertido em texto bruto.
   - O pipeline registra falhas de extração, quando existirem.

3. **Leitura estruturada**
   - O Reader Agent cria um `SuperSummary`.
   - Esse resumo contém questão de pesquisa, metodologia, achados e técnicas estatísticas.

4. **Classificação**
   - O Classifier Agent identifica tema, ano, tipo de estudo, natureza da pesquisa, natureza dos dados, métodos estatísticos, métricas e aderência ao plano de ensino.

5. **Avaliação crítica**
   - O Critic Agent atribui notas inteiras de 1 a 5 para sete critérios.
   - Cada nota exige justificativa textual baseada em evidências.

6. **Busca de citações**
   - O pipeline consulta serviço externo ou cache local para obter número de citações.

7. **Cálculo do IFRD**
   - O indicador sintetiza qualidade, alinhamento, aprendizagem, replicabilidade, aplicabilidade e adequação ao aluno.

8. **Síntese temática**
   - O Synthesizer Agent analisa o conjunto dos artigos.
   - Ele identifica clusters e relações de sobreposição, continuidade e complementação.

9. **Exportação**
   - Os resultados são consolidados no Excel `classificacao_artigos.xlsx`.

## Roteiro Sugerido para Apresentação de 40 Minutos

### 1. Contexto e Objetivo - 4 min

- Explicar o enunciado do trabalho.
- Apresentar o objetivo: analisar os artigos apresentados em sala e discutir contribuição para aprendizagem.
- Apresentar H0 e H1.

### 2. Organização dos Dados - 4 min

- Mostrar a estrutura de pastas dos artigos.
- Explicar metadados, PDFs e planilha final.
- Destacar que 84 artigos foram processados.

### 3. Metodologia ADK e Agentes - 10 min

- Explicar por que usar pipeline multiagente.
- Mostrar Reader, Classifier, Critic e Synthesizer.
- Explicar o papel do `SuperSummary`.
- Explicar validação com Pydantic e saída estruturada.
- Mostrar que a IA não responde texto livre: ela preenche esquemas definidos.

### 4. Variáveis e Rubricas - 6 min

- Apresentar variáveis independentes e dependentes.
- Explicar rubricas de 1 a 5.
- Explicar IFRD e sua fórmula.

### 5. Caracterização Inicial - 6 min

- Mostrar distribuição por tipo de estudo.
- Mostrar natureza da pesquisa e natureza dos dados.
- Mostrar tipo de veículo.
- Mostrar cobertura da ementa.

### 6. Visualizações e Resultados Esperados - 6 min

- Mostrar gráficos de IFRD, rubricas, tópicos da ementa e replicabilidade.
- Destacar a tensão entre alto alinhamento/aprendizagem e baixa replicabilidade.

### 7. Discussão com o Professor - 4 min

- Explicar limites do estudo observacional.
- Perguntar se o professor espera teste estatístico sobre as notas do pipeline ou se será necessário coletar percepção dos alunos.
- Discutir se o IFRD é aceitável como indicador final.
- Validar quais gráficos devem entrar nos slides finais.

## Pontos Para Levar Como Pergunta ao Professor

- A hipótese H1 pode ser tratada como contribuição potencial para aprendizagem ou precisa de coleta direta com alunos?
- O professor espera um teste estatístico formal usando as notas de aprendizagem, ou uma análise descritiva é suficiente?
- O IFRD pode ser usado como indicador final do trabalho?
- A rubrica de replicabilidade deve ter o mesmo peso das demais ou precisa de destaque maior?
- A apresentação deve priorizar metodologia técnica do pipeline ou resultados analíticos dos artigos?
- A planilha completa deve ser entregue junto com os slides?

