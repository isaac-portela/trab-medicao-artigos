# Resumo

## Identificação

- Título: Unveiling Hybrid Cyclomatic Complexity: A Comprehensive Analysis and Evaluation as an Integral Feature in Automatic Defect Prediction Models
- Aluno: Gabriella Fernanda Silva Pinto
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2025
- Fonte / Evento / Periódico: arXiv preprint, arXiv:2504.00477
- DOI / URL: https://arxiv.org/abs/2504.00477

## Objetivo

Analisar a métrica Hybrid Cyclomatic Complexity (HCC) como medida de complexidade em programação orientada a objetos e avaliar sua utilidade como atributo em modelos automáticos de predição de defeitos.

## Problema investigado

Métricas tradicionais de complexidade de classe podem ignorar ou misturar indevidamente a complexidade herdada. O artigo investiga se somar a complexidade própria da classe com a complexidade herdada em uma única métrica, HCC, preserva informação útil para predição de defeitos ou se é melhor separar complexidade própria e herdada.

## Método

- Tipo de estudo: estudo experimental quantitativo com análise de métricas de software e modelos de classificação para predição de defeitos.
- Dados/amostra: três conjuntos de dados Java: TinyBug, com 1151 arquivos (211 com defeitos e 940 sem defeitos); PROMISE, com 3473 arquivos (1440 com defeitos e 2033 sem defeitos); Unified, união dos dois, com 4624 arquivos (1651 com defeitos e 2973 sem defeitos).
- Procedimento: foram removidas classes em que WMC era igual a HCC; o número de bugs foi normalizado para classificação binária (com/sem defeito); os dados foram divididos em treino e teste na proporção 70/30, com amostragem do Pandas e random state igual a 1.
- Métricas/modelos/instrumentos: HCC, WMC, IWMC, DIT e LCOM. Foram comparadas duas representações: HCC-LCOM-DIT e WMC-LCOM-DIT-IWMC. O modelo de predição usou Support Vector Machine, especificamente C-Support Vector Classification do scikit-learn, kernel linear e C padrão 1.0. A normalização usou StandardScaler.
- Técnicas estatísticas: análise exploratória com distribuição KDE; análise de correlação entre métricas; avaliação de desempenho por precisão, recall e acurácia.

## Principais resultados

- Resultado 1: a complexidade herdada (IWMC) não se mostrou correlacionada com a complexidade própria da classe, o que sustenta a validade conceitual da HCC como métrica composta.
- Resultado 2: a representação que separa WMC e IWMC teve melhor acurácia nos três datasets: 0,5793 contra 0,5476 no TinyBug; 0,5514 contra 0,5282 no PROMISE; e 0,5666 contra 0,5535 no Unified.
- Resultado 3: o recall para classes defeituosas melhorou quando IWMC foi usado como atributo separado, indicando que a complexidade herdada contém sinal relevante para identificar defeitos.

## Contribuições

O artigo aprofunda a definição e a avaliação da HCC, mostrando que a complexidade herdada deve ser tratada explicitamente em métricas orientadas a objetos. Também evidencia que, em modelos de predição de defeitos, separar complexidade própria e herdada pode preservar informação que uma métrica agregada pode ocultar.

## Limitações

A validade interna depende da suposição de que classes em árvores de herança profundas têm maior propensão a erro por acumularem complexidade herdada. A validade externa é limitada pelo uso de datasets de origens diferentes: no TinyBug sabe-se que métricas foram calculadas com Checkstyle, mas no PROMISE não há informação suficiente sobre o processo de cálculo, o que pode gerar diferenças de definição entre bases.

## Relação com a disciplina

- Medição: discute a definição de métricas de complexidade, especialmente HCC, WMC, IWMC, DIT e LCOM, e como elas quantificam atributos internos de classes.
- Análise de Medições: compara correlações e desempenho preditivo das métricas, avaliando se a agregação em HCC perde informação frente ao uso separado de WMC e IWMC.
- Experimentação: usa datasets públicos, divisão treino/teste, modelo SVM e critérios objetivos de desempenho para testar hipóteses sobre métricas em predição de defeitos.

## Potencial para o trabalho final

O artigo pode apoiar um trabalho final sobre métricas de complexidade e predição de defeitos. Uma continuação viável seria aplicar HCC, WMC e IWMC em um projeto Java real, comparar os resultados com histórico de bugs e discutir se a complexidade herdada melhora a identificação de classes críticas.

## Citação curta

Cernău, Dioșan e Șerban (2025) indicam que a complexidade herdada é um fator relevante para predição de defeitos e deve ser distinguida da complexidade própria da classe.
