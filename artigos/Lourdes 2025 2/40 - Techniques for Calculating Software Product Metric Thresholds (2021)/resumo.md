# Resumo

## Identificação
- Título: Techniques for Calculating Software Product Metrics Threshold Values: A Systematic Mapping Study
- Aluno: Lucas Ferreira Garcia
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2021
- Fonte / Evento / Periódico: Applied Sciences, v. 11, n. 23, artigo 11377
- DOI / URL: https://doi.org/10.3390/app112311377 / https://www.mdpi.com/2076-3417/11/23/11377

## Objetivo

Investigar sistematicamente as técnicas usadas para calcular valores limiares de métricas de produto de software, especialmente métricas orientadas a objetos, e mapear métodos, atributos de qualidade, combinações de métricas, tipos de estudo e métricas correlacionadas com qualidade.

## Problema investigado

Métricas de software sem valores de referência ou limiares têm utilidade limitada para avaliar qualidade, identificar classes problemáticas, prever defeitos ou orientar manutenção. A literatura apresenta várias técnicas de derivação de limiares, mas faltava uma visão organizada sobre métodos, evidências, métricas usadas e lacunas de validação.

## Método
- Tipo de estudo: Estudo de mapeamento sistemático.
- Dados / amostra: 238 resultados iniciais em bases eletrônicas, 103 estudos inicialmente selecionados e 45 publicações finais após critérios de inclusão, exclusão e avaliação de qualidade.
- Procedimento: Foram definidas questões de pesquisa, strings de busca e critérios de seleção. As buscas cobriram IEEE Xplore, ScienceDirect, Springer, Wiley, ACM e estudos adicionais. Os artigos foram triados por título, resumo, conclusão e, quando necessário, texto completo. Os estudos finais foram classificados em uma planilha segundo atributos como método de cálculo, atributo de qualidade, categorias de métricas, tipo de estudo e métricas relevantes.
- Métricas, modelos ou instrumentos utilizados: Métricas orientadas a objetos, principalmente CK (WMC, DIT, NOC, CBO, RFC e LCOM), além de LOC, métricas de McCabe, Li, Lorenz e Kidd, Martin, QMOOD, Halstead, coesão, acoplamento, complexidade, tamanho e métricas de bad smells.
- Técnicas estatísticas, quando houver: Técnicas baseadas em propriedades estatísticas, percentis, transformação logarítmica, regressão logística, curvas ROC, sensibilidade, especificidade, área sob a curva, benchmarking, aprendizado de máquina e métodos baseados em distribuição.

## Principais resultados
- Resultado 1: As técnicas de cálculo de limiares foram agrupadas em experiência de programadores, propriedades estatísticas, abordagens relacionadas a atributos de qualidade e estudos de revisão; as técnicas estatísticas foram as mais frequentes.
- Resultado 2: Os atributos de qualidade mais investigados foram detecção de defeitos, detecção de bad smells e problemas de projeto; 16 estudos trataram detecção de defeitos, 6 trataram bad smells, 10 trataram problemas de design, 1 tratou propensão a reúso e 12 não validaram limiares contra atributos de qualidade.
- Resultado 3: As métricas CK foram as mais usadas, isoladamente ou combinadas com LOC e outras métricas, mas os limiares variaram entre sistemas, ferramentas e técnicas, indicando falta de consistência e necessidade de validação comparativa.

## Contribuições

O artigo oferece um catálogo estruturado de técnicas de cálculo de limiares para métricas de produto de software, sintetiza o estado da pesquisa, identifica quais métricas e atributos de qualidade são mais estudados e aponta lacunas para trabalhos futuros, como técnicas multivariadas, estudos industriais, comparação em datasets comuns e combinação de métricas estáticas com dados de qualidade.

## Limitações

As buscas foram restritas a bases eletrônicas conhecidas e podem ter deixado estudos relevantes de fora. A separação entre estudos de limiares e estudos de predição de qualidade nem sempre é clara. A avaliação de qualidade e a seleção de estudos podem conter viés dos revisores. O próprio campo também sofre com dados incompletos de defeitos, refatorações e atributos de qualidade, especialmente fora de projetos open source.

## Relação com a disciplina
Conexão com:
- Medição em Engenharia de Software: O artigo trata diretamente de métricas de produto, definição de limiares e interpretação de valores medidos para avaliar qualidade de software.
- Análise de Medições de Software: O foco está na análise estatística e empírica de medições, incluindo distribuição dos dados, correlação com atributos de qualidade, curvas ROC, regressão e comparação de técnicas de derivação.
- Experimentação em Engenharia de Software: O estudo é evidência secundária e mostra a importância de validação empírica, replicação, uso de bases comuns, controle de ferramentas de medição e avaliação de limiares contra atributos como defeitos, manutenção, segurança e desempenho.

## Potencial para o trabalho final

O artigo é uma base forte para um trabalho final sobre cálculo e validação de limiares de métricas de software. Ele pode orientar a escolha de métricas CK, LOC ou complexidade, a seleção de técnicas como percentis, ROC ou regressão logística, e a comparação de limiares em projetos reais ou repositórios open source.

## Citação curta

Limiares tornam métricas de software acionáveis, mas sua derivação depende de técnica, contexto, ferramenta de medição e validação empírica contra atributos de qualidade.
