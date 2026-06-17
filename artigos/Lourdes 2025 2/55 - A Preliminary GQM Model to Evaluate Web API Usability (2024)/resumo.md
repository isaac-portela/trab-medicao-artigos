# Resumo

## Identificacao

- Titulo: A Preliminary GQM Model to Evaluate Web API Usability
- Autores: Ariel Machini e Sandra Casas
- Ano: 2024
- Fonte: ASSE, Simposio Argentino de Ingenieria de Software, 53 JAIIO
- Aluno: Pedro Henrique Braga de Castro
- Link original: https://sedici.unlp.edu.ar/handle/10915/178461

## Objetivo

O artigo propoe um modelo preliminar baseado em GQM (Goal-Question-Metric) para avaliar a usabilidade de Web APIs. A intencao e organizar metas, perguntas e metricas de avaliacao de forma padronizada, facilitando a analise de fatores que afetam a experiencia de consumidores e desenvolvedores de APIs.

## Problema investigado

Os autores partem da importancia crescente das Web APIs na economia de APIs e no desenvolvimento moderno de software. Apesar de a usabilidade ser um atributo relevante de qualidade, a literatura ainda apresentava pouca padronizacao para avaliar especificamente a usabilidade de Web APIs. Muitas metricas existentes vinham de estudos sobre APIs locais, documentacao ou atributos isolados, sem um modelo integrado que relacionasse metricas a caracteristicas de usabilidade.

## Metodo

O estudo segue a abordagem Design Science Research para construir o artefato de avaliacao. O processo incluiu identificacao do problema, definicao do objetivo, desenvolvimento do modelo com GQM e avaliacao inicial por survey. Na construcao do modelo, os autores coletaram metricas de revisao de literatura, mapearam metricas de APIs locais para Web APIs quando possivel, buscaram metricas adicionais em guias e materiais tecnicos da industria, agruparam metricas por atributos de usabilidade e organizaram o resultado nos tres niveis do GQM: metas, perguntas e metricas.

O modelo final preliminar contem 6 metas, 8 perguntas e 32 metricas. A avaliacao foi feita com 36 participantes, principalmente desenvolvedores com experiencia em Web APIs, que julgaram em escala de 1 a 5 a influencia das metricas sobre a usabilidade.

## Principais resultados

O survey indicou que quase todas as metricas foram consideradas relevantes: apenas a metrica sobre numero de parametros consecutivos do mesmo tipo recebeu mediana inferior a 3. As metricas com maior importancia envolveram documentacao de elementos da API, clareza de nomes, exemplos de uso, informacoes de erro na documentacao, identificacao de elementos depreciados, especificidade de tipos de dados, similaridade e consistencia de nomes, quantidade de parametros e valores retornados, uso adequado de headers, suporte a filtragem/paginacao/ordenacao e erros HTTP 5XX.

Os autores tambem observaram que a maior parte das metricas se concentra em aprendibilidade, compreensibilidade e conhecimento da API, sugerindo que esses atributos sao centrais para a usabilidade de Web APIs. O conjunto de metricas ficou dividido entre 16 metricas objetivas e 16 subjetivas, o que implica que a aplicacao do modelo exige diferentes formas de coleta e interpretacao.

## Contribuicoes

A principal contribuicao e a organizacao de metricas dispersas em um modelo GQM voltado especificamente a Web APIs. O artigo tambem contribui ao relacionar metricas a atributos de usabilidade, explicitar a necessidade de combinar medidas objetivas e subjetivas e oferecer uma base inicial para avaliacao mais sistematica da experiencia de uso de APIs.

## Limitacoes

O modelo ainda e preliminar. A validacao empirica avaliou apenas o nivel quantitativo, isto e, as metricas, deixando os niveis conceitual e operacional para validacoes futuras. A amostra do survey foi limitada, com predominancia de participantes de paises hispanofalantes e perfis tecnicos especificos. Os autores tambem indicam que as metricas ainda nao possuem pesos definidos e que novas entrevistas e validacoes com especialistas sao necessarias.

## Relacao com a disciplina

O artigo se relaciona diretamente com medicao e avaliacao de qualidade de software, pois aplica GQM para transformar objetivos abstratos de usabilidade em perguntas e metricas observaveis. Ele mostra como atributos de qualidade podem ser operacionalizados e como a escolha de metricas depende do contexto, do objeto medido e do ponto de vista dos usuarios.

## Potencial para o trabalho final

O artigo tem alto potencial para um trabalho final sobre metricas de qualidade, usabilidade ou avaliacao de APIs. O modelo pode ser usado como base para criar um checklist de avaliacao de uma API real, comparar APIs diferentes ou propor uma extensao com pesos, coleta automatizada de metricas e validacao pratica. Tambem pode apoiar um estudo sobre a aplicacao do GQM em atributos de qualidade nao funcionais.

## Citacao curta

Machini e Casas (2024) propoem um modelo GQM preliminar com 6 metas, 8 perguntas e 32 metricas para avaliar a usabilidade de Web APIs, destacando a importancia de documentacao, clareza de nomes, tratamento de erros e suporte a tarefas comuns do usuario.

## Ruido de extracao

A extracao textual foi legivel, mas apresentou ruido moderado em acentuacao, hifenizacao, separacao de palavras e cabecalhos/rodapes repetidos do evento. As figuras e a hierarquia visual do modelo foram extraidas apenas parcialmente como texto, entao a sintese priorizou os trechos textuais de metodo, avaliacao, discussao e conclusao.
