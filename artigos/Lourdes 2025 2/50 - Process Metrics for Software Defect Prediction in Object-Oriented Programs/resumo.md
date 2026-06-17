# Resumo

## Identificação

- Título: Process metrics for software defect prediction in object-oriented programs
- Autores: Qiao Yu, Shujuan Jiang, Junyan Qian, Lili Bo, Li Jiang e Gongjie Zhang
- Ano: 2020
- Periódico: IET Software
- DOI: 10.1049/iet-sen.2018.5439
- Aluno: Gabriel Henrique Silva Pereira
- Grupo: Lourdes 2025/2
- Link original: https://www-periodicos-capes-gov-br.ez93.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&amp;source=all&amp;id=W3001993719

## Objetivo

Propor e avaliar métricas de processo baseadas na evolução de programas orientados a objetos para melhorar a predição de defeitos em versões sucessivas de software.

## Problema investigado

Métodos tradicionais de predição de defeitos usam principalmente métricas de código, que descrevem características estáticas do software. O problema é que defeitos também surgem e se redistribuem durante a evolução do sistema, quando classes são alteradas, defeitos antigos são corrigidos e novas demandas são implementadas. Assim, apenas métricas estáticas podem ser insuficientes para prever defeitos em versões evolutivas.

## Método

Os autores propõem duas métricas de processo. A primeira, pcdc, usa a taxa de defeitos de pacotes na versão anterior para estimar a probabilidade de uma classe ser defeituosa na versão atual. A segunda, pccm, mede a porcentagem de métricas de código que mudaram em uma classe entre duas versões vizinhas, representando seu grau de mudança.

O estudo empírico usa 33 versões de nove projetos Java de código aberto do repositório Tera-PROMISE. As classes comuns entre versões vizinhas são identificadas por correspondência exata de nome de pacote e nome de classe. Os autores comparam métricas de código, métricas de código combinadas com code churn e métricas de código combinadas com as métricas propostas. Os modelos usados são K-nearest neighbours, regressão logística e naive Bayes, com AUC como métrica principal de desempenho.

## Principais resultados

Os resultados indicam que as métricas propostas melhoram a predição de defeitos em vários cenários, especialmente quando as taxas de defeito dos pacotes permanecem relativamente estáveis entre versões vizinhas. O estudo também mostra que há correlação entre taxas de defeito de pacotes em versões consecutivas em parte relevante dos projetos analisados. A combinação das duas métricas propostas tende a ser equivalente ou ligeiramente superior ao uso isolado de pcdc, e geralmente melhor ou equivalente ao uso isolado de pccm. A eficácia, porém, varia conforme o projeto, o modelo de predição e a estabilidade das taxas de defeito.

## Contribuições

- Propõe duas métricas de processo para programas orientados a objetos: pcdc e pccm.
- Mostra como incorporar dados de evolução entre versões vizinhas em conjuntos de treinamento e teste.
- Compara as métricas propostas com métricas de código e métricas de churn em múltiplos projetos e versões.
- Evidencia que dados históricos recentes podem melhorar a predição de defeitos quando o padrão de evolução do projeto é relativamente estável.

## Limitações

As métricas dependem da existência de classes comuns entre versões vizinhas, o que reduz sua aplicabilidade para classes novas ou para projetos com refatorações intensas. A identificação de classes comuns usa correspondência textual exata, o que pode não capturar renomeações ou movimentações entre pacotes. Os experimentos usam apenas projetos Java de código aberto e três modelos de classificação; os próprios autores indicam a necessidade de avaliar mais bases de dados, mais modelos e formas de extrair métricas de múltiplas versões históricas.

## Relação com a disciplina

O artigo se relaciona com medição de software ao transformar características do processo de evolução em métricas quantitativas usadas para avaliar risco de defeito. Ele ilustra como definir, coletar, comparar e validar métricas em um contexto empírico, além de mostrar a importância de escolher medidas adequadas ao objetivo da análise.

## Potencial para o trabalho final

O artigo tem bom potencial para um trabalho final sobre métricas de software, qualidade, manutenção ou predição de defeitos. Ele pode ser usado como referência para discutir métricas de produto versus métricas de processo, desenho de estudos empíricos com versões sucessivas e avaliação de modelos por AUC. Também oferece uma possível base para replicação parcial ou comparação com outros conjuntos de métricas.

## Citação curta

Yu et al. (2020) mostram que métricas de processo baseadas na taxa histórica de defeitos de pacotes e no grau de mudança das classes podem melhorar a predição de defeitos em programas orientados a objetos, sobretudo em projetos com evolução estável.

