# Resumo

## Identificação
- Título: Software Development and Maintenance Effort Estimation Using Function Points and Simpler Functional Measures
- Aluno: Thiago Vitor Pereira Perdigao
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2024
- Fonte / Evento / Periódico: Software, MDPI, volume 3, número 4, páginas 442-472
- DOI / URL: https://doi.org/10.3390/software3040022

## Objetivo

Avaliar se medidas funcionais simplificadas, especialmente Simple Function Points (SFPs) e sua componente transacional (tSFPs), estimam esforço de desenvolvimento e manutenção com acurácia comparável aos Function Points não ajustados (UFPs), inclusive em projetos considerados mais complexos.

## Problema investigado

O artigo investiga a crença prática de que UFPs seriam superiores para estimar esforço em projetos complexos porque incorporam a complexidade de transações e arquivos lógicos, enquanto medidas simplificadas ignoram parte desses detalhes. A questão central é saber se essa complexidade adicional realmente melhora a acurácia da estimativa.

## Método
- Tipo de estudo: Estudo empírico quantitativo com dados históricos de projetos reais.
- Dados / amostra: Visão customizada do dataset ISBSG com 1307 projetos de alta qualidade; a análise inclui 533 projetos de novo desenvolvimento, 128 extensões e 646 melhorias/enhancements.
- Procedimento: Os autores calcularam UFP, SFP e tSFP para cada projeto, separaram os dados por tipo de projeto e por nível de complexidade, e compararam o erro de estimativa produzido por cada medida funcional.
- Métricas, modelos ou instrumentos utilizados: UFPs, SFPs, tSFPs, esforço em PersonHours, produtividade como Size/Effort, modelo simples Effort = Size/Productivity, erro de estimativa, erro absoluto médio (MAR) e erro absoluto mediano (MdAR).
- Técnicas estatísticas, quando houver: Teste de sinais com teste binomial, alfa = 0,05, comparação par a par entre medidas e tratamento de empates quando a diferença entre erros foi menor que 1% do esforço real.

## Principais resultados
- Resultado 1: Quando a complexidade não é considerada, SFPs e tSFPs fornecem estimativas tão acuradas quanto UFPs na maior parte das comparações; 15 de 24 casos indicaram equivalência.
- Resultado 2: Para projetos de alta ou baixa complexidade, UFPs e medidas simplificadas geralmente apresentam níveis equivalentes de acurácia; a principal exceção é que UFPs parecem preferíveis a SFPs em projetos de alta complexidade quando se usa produtividade média.
- Resultado 3: A acurácia das estimativas diminui quando a complexidade aumenta, independentemente do tipo de projeto, da métrica funcional usada ou do cálculo de produtividade, sugerindo que nem UFPs nem medidas simplificadas capturam bem a complexidade relevante para esforço.

## Contribuições

O estudo amplia evidências anteriores ao incluir, além de novos desenvolvimentos, projetos de extensão e enhancement. Ele questiona a suposição de que a complexidade embutida nos Function Points tradicionais melhora sistematicamente a estimativa de esforço e mostra que medidas mais simples podem ser competitivas, especialmente quando requisitos completos ainda não estão disponíveis.

## Limitações

Os resultados dependem do dataset ISBSG e de uma visão customizada com campos específicos; ainda assim, a generalização fora desse benchmark requer novos estudos. O modelo de esforço é deliberadamente simples e considera apenas tamanho funcional e produtividade. A noção de complexidade é a da análise de Function Points, não outras formas de complexidade de software, como complexidade ciclomática. Os achados também não se aplicam diretamente a métodos como COSMIC, que não tratam complexidade da mesma forma.

## Relação com a disciplina
Conexão com:
- Medição em Engenharia de Software: O artigo trata diretamente de medição funcional de software, comparando UFP, SFP e tSFP como medidas de tamanho para estimativa de esforço.
- Análise de Medições de Software: O estudo analisa erros de estimativa, produtividade, distribuição por complexidade e comparação estatística entre métricas.
- Experimentação em Engenharia de Software: Embora não seja um experimento controlado com participantes, é um estudo empírico quantitativo com questões de pesquisa explícitas, dados reais, critérios de seleção, ameaças à validade e testes estatísticos.

## Potencial para o trabalho final

O artigo é adequado para um trabalho final sobre métricas funcionais, estimativa de esforço, comparação de modelos simples de medição e validade prática de medidas simplificadas. Também pode servir como base para discutir custo-benefício entre precisão de medição e simplicidade de coleta em ambientes ágeis ou em fases iniciais de projeto.

## Citação curta

Lavazza, Locoro e Meli (2024) mostram, com dados do ISBSG, que medidas funcionais simplificadas geralmente estimam esforço com acurácia comparável aos UFPs, e que a complexidade continua prejudicando a acurácia independentemente da métrica usada.
