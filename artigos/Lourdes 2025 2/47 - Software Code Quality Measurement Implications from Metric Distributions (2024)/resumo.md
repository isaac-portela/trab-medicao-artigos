# Resumo

## Identificação

**Título:** Software Code Quality Measurement: Implications from Metric Distributions

**Aluno:** Gabriel Pongelupe de Carvalho

**Grupo:** Lourdes 2025/2

**Arquivo:** artigo.pdf

**Ano:** 2024

**Fonte / Evento / Periódico:** arXiv preprint, arXiv:2307.12082v4

**DOI / URL:** https://arxiv.org/pdf/2307.12082

## Objetivo

Propor uma forma consistente de avaliar métricas de qualidade de código, incluindo métricas monotônicas e não monotônicas, usando distribuições observadas em repositórios open source de alta adoção como referência para gerar pontuações de 0 a 100.

## Problema investigado

O artigo parte do problema de que empresas usam muitas métricas de qualidade de código, mas não há um padrão consistente para interpretá-las. Algumas métricas têm relação monotônica com qualidade, como violações ou code smells, enquanto outras não têm uma direção simples, como complexidade ciclomática, comentários ou coesão. Isso dificulta comparar projetos e transformar medidas brutas em avaliações úteis.

## Método

**Tipo de estudo:** Estudo empírico quantitativo com proposta de método de mensuração.

**Dados/amostra:** 36.460 repositórios GitHub de alta popularidade, em Java, Python, JavaScript e TypeScript, totalizando mais de 600 milhões de linhas de código. A amostra foi filtrada para remover repositórios que não eram de engenharia.

**Procedimento:** Os autores coletaram repositórios de alto número de estrelas, extraíram métricas com SonarQube e CK, normalizaram métricas por tamanho ou estrutura do repositório e ajustaram distribuições para cada métrica e linguagem. Depois converteram valores brutos em pontuações por funções baseadas em CDF e testaram a capacidade explicativa dessas pontuações sobre adoção em OSS, medida por estrelas.

**Métricas/modelos/instrumentos:** 20 métricas associadas a manutenibilidade, confiabilidade e funcionalidade. Exemplos: complexidade ciclomática, complexidade cognitiva, file complexity, code smells, acoplamento, fan-in, fan-out, violações totais/críticas/informativas, linhas a cobrir, linhas comentadas, blocos/arquivos/linhas duplicadas. Foram usados SonarQube, CK, modelos exponenciais para métricas monotônicas, modelos gaussianos assimétricos para métricas não monotônicas e Gradient Boosting Classifier para derivar pesos de importância.

**Técnicas estatísticas:** Ajuste de distribuições de probabilidade, funções de distribuição acumulada, normalização de métricas, classificação supervisionada com divisão treino/validação 4:1, importância de atributos, acurácia, precisão, recall, F1, AUC ROC e R2.

## Principais resultados

**Resultado 1:** A distinção entre métricas monotônicas e não monotônicas permite tratar medidas de qualidade de forma mais coerente. Métricas como code smells e violações se ajustam bem a distribuições exponenciais, enquanto complexidade ciclomática e complexidade cognitiva seguem melhor distribuições gaussianas assimétricas.

**Resultado 2:** As pontuações derivadas das distribuições apresentaram boa capacidade de explicar adoção em OSS. Para Java, os resultados foram especialmente fortes: acurácia de 0,947, AUC ROC de 0,946 e R2 de 0,787. Para JavaScript, Python e TypeScript, a explicação foi menor, com R2 de 0,274, 0,186 e 0,247.

**Resultado 3:** File Complexity foi a métrica de maior peso na dimensão de manutenibilidade nas quatro linguagens. Em confiabilidade, Total Violations foi mais importante para Java, enquanto Critical Violations foi mais importante nas outras linguagens. Em funcionalidade, Comment Lines teve peso relevante, especialmente em Java.

## Contribuições

O artigo contribui ao transformar métricas brutas em pontuações comparáveis, ao mostrar que nem toda métrica de qualidade deve ser interpretada como "quanto menor, melhor" e ao conectar a avaliação de qualidade de código com adoção de software open source. A proposta também oferece um caminho prático para organizações criarem benchmarks internos a partir de distribuições de projetos considerados bons.

## Limitações

Os autores reconhecem que a efetividade do método ainda não foi sistematicamente validada. Os parâmetros das distribuições são sensíveis aos dados usados como referência, o que exige amostras amplas e bem filtradas. Há também limitações instrumentais: algumas métricas só foram extraídas para Java, e o campo Line to Cover apareceu com valor zero nos dados brutos, possivelmente por problema de coleta ou baixa disponibilidade de informação de testes nos repositórios OSS.

## Relação com a disciplina

**Medição:** O artigo é diretamente ligado à definição, operacionalização e interpretação de métricas de software. Ele mostra que a utilidade de uma métrica depende de sua escala, normalização, distribuição e relação com o construto qualidade.

**Análise de Medições:** A contribuição principal está na análise estatística das distribuições de métricas e na conversão de valores brutos em escores interpretáveis. O trabalho também discute pesos por importância e avaliação da capacidade explicativa das medições.

**Experimentação:** Embora não seja um experimento controlado, o estudo usa desenho empírico com grande amostra, treinamento/validação e avaliação quantitativa de desempenho dos modelos. Pode ser discutido como estudo observacional com hipótese de relação entre qualidade medida e adoção.

## Potencial para o trabalho final

O artigo pode sustentar um trabalho final sobre construção de indicadores de qualidade de código. Uma aplicação viável seria coletar métricas de projetos reais, ajustar distribuições ou usar parâmetros do artigo como referência, comparar pontuações entre projetos e discutir quais métricas têm interpretação monotônica ou não monotônica. Também pode servir como base para avaliar se métricas de qualidade explicam popularidade, manutenção ou defeitos em um conjunto menor de repositórios.

## Citação curta

Jin et al. (2024) defendem que medir qualidade de código exige tratar separadamente métricas monotônicas e não monotônicas, convertendo-as em escores baseados em distribuições.
