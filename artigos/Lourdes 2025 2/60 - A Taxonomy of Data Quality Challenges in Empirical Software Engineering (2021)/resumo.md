# Resumo

## Identificação

- Aluno: Miguel Vieira de Souza
- Grupo: Lourdes 2025/2
- Artigo: "A Taxonomy of Data Quality Challenges in Empirical Software Engineering"
- Autores: Michael Franklin Bosu e Stephen G. MacDonell
- Publicação: Proceedings of the 22nd Australasian Software Engineering Conference, 2013
- Link original: https://arxiv.org/abs/2106.06141

## Objetivo

O artigo tem como objetivo propor uma taxonomia de desafios de qualidade de dados em engenharia de software empírica. A intenção é aumentar a consciência da comunidade sobre problemas que afetam conjuntos de dados usados em modelos de estimativa de esforço, predição de defeitos, classificação e outras análises quantitativas.

## Problema investigado

O problema investigado é que modelos empíricos em engenharia de software dependem fortemente da qualidade dos dados usados para construí-los. Dados com ruído, lacunas, inconsistências, baixa relevância ou origem pouco confiável podem gerar modelos incorretos, pouco replicáveis ou inadequados para apoiar decisões reais. O artigo também destaca que a área costuma dar mais atenção aos algoritmos e modelos do que à qualidade e à proveniência dos dados.

## Método

Os autores revisaram a literatura sobre qualidade de dados em engenharia de software empírica e áreas relacionadas. A partir dessa revisão, organizaram os problemas encontrados em uma taxonomia com três classes principais: accuracy, relevance e provenance. O artigo discute estudos representativos para cada elemento da taxonomia e, na discussão, contabiliza 57 artigos que tratavam de algum aspecto de qualidade de dados, identificando 74 ocorrências de problemas de qualidade.

## Principais resultados

A taxonomia proposta divide os desafios em três grupos. A classe accuracy inclui ruído, outliers, incompletude, inconsistência e redundância, ou seja, problemas que tornam os dados inadequados para modelagem. A classe relevance cobre heterogeneidade, quantidade de dados e atualidade, tratando da adequação de um conjunto de dados para aplicação de modelos em diferentes contextos. A classe provenance inclui sensibilidade comercial, acessibilidade e confiabilidade, abordando fatores que limitam acesso, rastreabilidade e confiança nos dados.

Na revisão, problemas de accuracy receberam a maior atenção, com 65% das ocorrências, seguidos por relevance, com 23%, e provenance, com apenas 12%. Dentro de accuracy, ruído e incompletude foram os temas mais frequentes. Em relevance, heterogeneidade e tamanho do conjunto de dados foram os pontos mais discutidos. Provenance foi a área menos explorada, embora os autores defendam que ela é essencial para melhorar confiança, replicabilidade e interpretação dos resultados.

## Contribuições

A principal contribuição é uma taxonomia clara para organizar problemas de qualidade de dados em engenharia de software empírica. O artigo também evidencia que a área trata qualidade de dados de forma fragmentada e que nenhum estudo revisado avaliou todos os aspectos da taxonomia. Outra contribuição importante é a defesa de sistemas de proveniência para registrar origem, coleta, transformação e uso dos dados, permitindo investigar causas de problemas e prevenir erros na fonte.

## Limitações

O estudo é baseado em revisão de literatura e depende da cobertura dos artigos selecionados. As categorias propostas organizam o conhecimento existente, mas não são validadas por aplicação ampla em projetos industriais. Os próprios autores apontam que quase todos os estudos analisados vêm de instituições acadêmicas, havendo pouca evidência sobre como esses problemas afetam a prática industrial de engenharia de software.

## Relação com a disciplina

O artigo tem relação direta com medição de software, engenharia de software empírica, qualidade de dados, construção de modelos preditivos e validade de estudos quantitativos. Ele mostra que métricas e modelos só são úteis quando os dados de entrada são confiáveis, relevantes e rastreáveis.

## Potencial para o trabalho final

O artigo pode fundamentar um trabalho final sobre qualidade de dados em medições de software, validade de modelos de predição, limpeza de bases de métricas ou uso de proveniência para melhorar estudos empíricos. Também serve como referência para criar critérios de avaliação de bases de dados antes da aplicação de técnicas estatísticas ou de aprendizado de máquina.

## Citação curta

Bosu e MacDonell propõem uma taxonomia de qualidade de dados para engenharia de software empírica, agrupando desafios em accuracy, relevance e provenance, e mostram que a área ainda explora pouco a proveniência, apesar de sua importância para confiança e replicabilidade.
