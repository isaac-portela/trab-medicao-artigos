# Resumo

## Identificação
- Título: Robust Statistical Methods for Empirical Software Engineering
- Aluno: Matheus Vinicius Mota Rodrigues
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2016
- Fonte / Evento / Periódico: Empirical Software Engineering, 22, 579-630
- DOI / URL: DOI 10.1007/s10664-016-9437-5; https://www.researchgate.net/publication/303640350_Robust_Statistical_Methods_for_Empirical_Software_Engineering

## Objetivo

Atualizar a orientação estatística usada em Engenharia de Software Empírica, mostrando por que métodos clássicos podem falhar com dados reais não normais e apresentando métodos robustos, com exemplos trabalhados e uma reanálise de um experimento multi-site.

## Problema investigado

O artigo investiga o risco de pesquisadores aplicarem testes paramétricos e não paramétricos convencionais, como teste t, ANOVA, Mann-Whitney-Wilcoxon e Kruskal-Wallis, em dados de software com assimetria, caudas longas, outliers, variâncias instáveis, escalas ordinais ou amostras pequenas. Nessas condições, os níveis reais de erro tipo I, poder estatístico e tamanhos de efeito podem ser inadequados.

## Método
- Tipo de estudo: Artigo metodológico com síntese de literatura estatística, exemplos reprodutíveis e reanálise de dados de Engenharia de Software.
- Dados / amostra: Quatro conjuntos de dados de software usados como exemplos, incluindo esforço de projetos finlandeses, dados COCOMO de produtividade, dados de predição de defeitos e dados de um experimento multi-site sobre abstracts estruturados e convencionais.
- Procedimento: Os autores revisam evidências sobre falhas de métodos clássicos sob não normalidade, apresentam alternativas robustas e demonstram sua aplicação em dados reais, especialmente no experimento multi-site sobre clareza e completude de abstracts.
- Métricas, modelos ou instrumentos utilizados: Distribuições empíricas, medidas de localização e escala, médias aparadas, médias winsorizadas, medianas, estimadores robustos, produtividade, completude e clareza de abstracts, probabilidade de superioridade e tamanho de efeito.
- Técnicas estatísticas, quando houver: Gráficos de densidade kernel, teste de Welch, teste de Yuen com médias aparadas, métodos robustos baseados em ranks, Cliff's delta, método ANOVA-like de Brunner et al., intervalos de confiança robustos e análise de poder/erro tipo I discutida a partir da literatura.

## Principais resultados
- Resultado 1: Métodos clássicos baseados em teste t e F não são confiáveis quando os dados têm forte assimetria, caudas pesadas ou variâncias heterogêneas, situações comuns em dados empíricos de software.
- Resultado 2: Os autores recomendam gráficos de densidade kernel em vez de depender apenas de box plots, pois box plots podem esconder detalhes importantes da distribuição.
- Resultado 3: Para comparar localizações centrais, o artigo recomenda médias aparadas com teste de Yuen/Welch; para dados ordinais ou mudanças na distribuição como um todo, recomenda Cliff's delta, probabilidade de superioridade e métodos robustos baseados em ranks.

## Contribuições

O artigo fornece um guia prático para escolher métodos estatísticos robustos em Engenharia de Software Empírica, explica a teoria necessária em linguagem aplicada e disponibiliza exemplos reprodutíveis por meio do pacote R `reproducer`. Também reforça a importância de relatar tamanhos de efeito robustos, não apenas valores-p.

## Limitações

Métodos robustos podem ter menor poder quando os dados são realmente normais ou quando as amostras são grandes o suficiente para métodos clássicos funcionarem bem. O uso de trimming e de correções como Welch reduz graus de liberdade, tornando análise de poder e planejamento amostral mais complexos. Além disso, parte das decisões, como avaliar normalidade por gráficos de densidade kernel, ainda depende de julgamento do analista.

## Relação com a disciplina
Conexão com:
- Medição em Engenharia de Software: Mostra que métricas de software frequentemente geram distribuições assimétricas e com outliers, exigindo cuidado na escolha de medidas de localização, dispersão e tamanho de efeito.
- Análise de Medições de Software: Discute diretamente como analisar medições não normais, com alternativas robustas a testes tradicionais e visualizações mais informativas.
- Experimentação em Engenharia de Software: Apoia o desenho e a análise de experimentos com amostras pequenas, variâncias instáveis e dados ordinais, comuns em estudos com participantes humanos.

## Potencial para o trabalho final

O artigo é útil como referência metodológica para justificar escolhas estatísticas no trabalho final. Ele pode orientar a seleção de gráficos, testes robustos, tamanhos de efeito e análise de dados quando as métricas coletadas não seguirem normalidade ou envolverem amostras pequenas.

## Citação curta

Kitchenham et al. mostram que dados empíricos de software frequentemente violam pressupostos de testes clássicos e defendem métodos estatísticos robustos para obter conclusões mais confiáveis.
