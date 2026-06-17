# Resumo

## Identificação

- Título: Source Code Metrics for Software Defects Prediction
- Aluno: Renato Matos Alves Penna
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2023
- Fonte / Evento / Periódico: 38th ACM/SIGAPP Symposium on Applied Computing (SAC '23), Tallinn, Estonia
- DOI / URL: https://doi.org/10.1145/3555776.3577809; versão arXiv: https://arxiv.org/pdf/2301.08022

## Objetivo

O artigo avalia o uso de métricas de código-fonte como atributos em modelos de predição de defeitos e identifica quais métricas individuais contribuem mais ou menos para a classificação de classes defeituosas.

## Problema investigado

Estudos anteriores mostram resultados divergentes sobre a utilidade de métricas de código para predição de defeitos. Além disso, não há consenso sobre quais métricas são melhores preditoras, e muitas bases ou ferramentas usadas em trabalhos prévios são depreciadas, indisponíveis ou difíceis de replicar.

## Método

- Tipo de estudo: Estudo empírico de mineração de repositórios de software e classificação supervisionada.
- Dados/amostra: 39 projetos Java open source extraídos do GitHub, totalizando 275 versões em janelas de 6 meses.
- Procedimento: Mineração de repositórios e dados de issues/commits; cálculo de métricas em nível de classe; ligação de commits corretivos a classes modificadas; marcação binária das classes como defeituosas ou não defeituosas; divisão em treino e teste com validação cruzada estratificada de 10 folds.
- Métricas/modelos/instrumentos: 12 métricas de código: LOC; suíte CK com WMC, DIT, NOC, RFC, LCOM5 e CBO; suíte OTHER com NPA, NPM, NLE, CBOI e CD. Ferramentas e bibliotecas: PyGithub, PyDriller, SourceMeter e scikit-learn. Modelos: Naive Bayes, Decision Tree e Random Forest.
- Técnicas estatísticas: F-measure para a classe defeituosa, AUC-ROC ponderado, permutation feature importance com validação cruzada de 10 folds, Variance Inflation Factor (VIF) para multicolinearidade, Mann-Whitney U Test e Kruskal-Wallis One-Way ANOVA.

## Principais resultados

- Resultado 1: Decision Tree e Random Forest apresentaram os melhores desempenhos gerais para predição de defeitos, enquanto Naive Bayes teve desempenho inferior ou mais instável.
- Resultado 2: As suítes CK, OTHER e CK+OTHER superaram o uso isolado de LOC, indicando que conjuntos de métricas de código agregam informação útil aos classificadores.
- Resultado 3: NOC foi a métrica individual mais forte, seguida por NPA, DIT e LCOM5. CBO foi a pior preditora no conjunto analisado, seguida por CD e NPM.

## Contribuições

O estudo fornece evidência empírica sobre a utilidade de métricas de código em predição de defeitos em projetos Java reais. Também compara conjuntos de métricas, modelos de classificação e importância individual das métricas, tratando explicitamente multicolinearidade antes da análise de importância.

## Limitações

A identificação de defeitos depende de heurísticas baseadas em mensagens de commit e issues, o que pode deixar defeitos não mencionados fora da base. As versões são agregadas em intervalos de 6 meses, uma escolha necessária para obter dados suficientes, mas que pode perder precisão temporal. Os resultados se restringem a projetos Java open source e podem não generalizar para outros ecossistemas.

## Relação com a disciplina

- Medição: O artigo operacionaliza métricas de produto em nível de classe e mostra como elas podem representar tamanho, complexidade, acoplamento, coesão, herança e documentação.
- Análise de Medições: As métricas são analisadas como variáveis preditoras, com avaliação de desempenho, importância de atributos e controle de multicolinearidade.
- Experimentação: O desenho experimental compara modelos e conjuntos de métricas, usa validação cruzada e testes estatísticos para avaliar diferenças de desempenho.

## Potencial para o trabalho final

O artigo pode apoiar um trabalho final sobre predição de defeitos, comparação de métricas estáticas ou avaliação de modelos de machine learning em engenharia de software. O desenho pode ser replicado em outro conjunto de projetos, em outra linguagem ou com métricas adicionais de processo e mudança.

## Citação curta

Rebro, Rossi e Chren (2023) indicam que métricas de código melhoram a predição de defeitos, com NOC, NPA, DIT e LCOM5 entre as preditoras mais úteis.
