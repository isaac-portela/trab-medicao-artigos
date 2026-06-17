# Resumo

## Identificação

- Título: A Tool-Based Perspective on Software Code Maintainability Metrics: A Systematic Literature Review
- Aluno: João Pedro Queiroz Rocha
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2020
- Fonte / Evento / Periódico: Scientific Programming, Hindawi, Volume 2020, Article ID 8840389
- DOI / URL: https://doi.org/10.1155/2020/8840389

## Objetivo

O artigo busca organizar a literatura sobre métricas estáticas de manutenibilidade de código, identificar ferramentas disponíveis para calculá-las e relacionar métricas, ferramentas e linguagens de programação. O foco é apoiar pesquisadores e profissionais na escolha de conjuntos de métricas e ferramentas para avaliação de manutenibilidade.

## Problema investigado

A literatura propõe muitas métricas e modelos para avaliar ou predizer manutenibilidade, mas não há consenso sobre quais métricas são mais confiáveis nem sobre quais ferramentas cobrem essas métricas em diferentes linguagens. Também há lacunas de suporte para linguagens mais novas ou menos estudadas.

## Método

- Tipo de estudo: Revisão Sistemática da Literatura (SLR), seguindo diretrizes de Kitchenham/Charters para engenharia de software baseada em evidências.
- Dados/amostra: Busca em ACM Digital Library, IEEE Xplore, Scopus e Web of Science, considerando publicações entre 2000 e 2019. Após refinamento e remoção de duplicatas, foram reunidos 801 artigos candidatos e selecionados 43 estudos primários.
- Procedimento: Definição de questões de pesquisa pelo paradigma Goal-Question-Metric; construção e refinamento de strings de busca; aplicação de critérios de inclusão e exclusão; seleção independente pelos autores com escala Likert de 5 pontos; leitura de título, resumo e, quando necessário, texto completo; snowballing; extração manual padronizada em planilha.
- Métricas/modelos/instrumentos: Foram extraídas métricas, suítes de métricas, linguagens suportadas, ferramentas citadas, tipo de ferramenta (aberta/fechada) e métricas computadas. A revisão identificou 174 métricas, 15 métricas/suítes mais populares e 19 ferramentas de cálculo.
- Técnicas estatísticas: Síntese descritiva por contagem de menções, pontuação de opinião sobre métricas (+1 para uso/avaliação positiva, -1 para crítica), medianas de menções e escores, e análise de cobertura mínima de ferramentas por linguagem.

## Principais resultados

- Resultado 1: A revisão encontrou 174 métricas de manutenibilidade; depois de filtrar por menções e escore, destacou 15 métricas/suítes, incluindo CC, LOC, C&K, Halstead, MI, LCOM2, MPC, NOM, NPM, STAT e WMC.
- Resultado 2: Foram identificadas 19 ferramentas disponíveis ou citadas, incluindo ferramentas fechadas como CAST AIP, Understand, JHawk, CMT++/CMTJava e Visual Studio, e ferramentas abertas como CKJM, MetricsReloaded, SonarQube/CodeAnalyzers, eslint, escomplex, CCFinderX e Halstead Metrics Tool.
- Resultado 3: Com ferramentas abertas e fechadas, conjuntos ótimos de até 4 ferramentas cobrem as métricas mais populares em C, C++, C# e JavaScript, enquanto Java exige até 5 ferramentas. Usando apenas ferramentas abertas, a cobertura é incompleta; LCOM2 e MPC não foram explicitamente suportadas por ferramentas abertas analisadas.

## Contribuições

O trabalho consolida um catálogo de métricas de manutenibilidade, relaciona métricas a ferramentas e linguagens, e mostra combinações mínimas de ferramentas para maximizar cobertura. Também evidencia lacunas práticas: métricas populares sem bom suporte automatizado e maior cobertura em ferramentas fechadas do que em ferramentas abertas.

## Limitações

As conclusões dependem das bases, strings e critérios de busca definidos, ainda que o protocolo seja reprodutível. A extração e a pontuação das métricas envolveram julgamento manual dos autores. A generalização é limitada às linguagens e estudos primários encontrados; métricas dinâmicas ficaram fora do escopo.

## Relação com a disciplina

- Medição: O artigo é diretamente centrado na definição, seleção e operacionalização de métricas de software, especialmente métricas estáticas de produto para manutenibilidade.
- Análise de Medições: A revisão compara frequência, escore e cobertura das métricas, mostrando como dados de medição podem ser sintetizados para apoiar decisões.
- Experimentação: Embora não execute experimento controlado, segue um protocolo empírico secundário, com questões de pesquisa, critérios de seleção, extração replicável e análise de ameaças à validade.

## Potencial para o trabalho final

O artigo pode fundamentar um trabalho final sobre escolha de métricas de manutenibilidade e ferramentas de análise estática. Ele oferece uma base para comparar ferramentas em projetos reais, avaliar cobertura de métricas por linguagem ou propor um conjunto reduzido de métricas aplicáveis em estudos práticos.

## Citação curta

Ardito et al. (2020) mostram que a avaliação de manutenibilidade depende tanto da escolha das métricas quanto da cobertura real oferecida pelas ferramentas disponíveis.
