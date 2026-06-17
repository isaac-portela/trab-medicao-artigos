# Resumo

## Identificação

- Título: Metrics for Evaluating and Improving Transparency in Software Engineering: An Empirical Study and Improvement Model
- Aluno: Gabriel Lourenço Reis Resende
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2024
- Fonte / Evento / Periódico: SN Computer Science, volume 5, artigo 1097
- DOI / URL: https://doi.org/10.1007/s42979-024-03471-3

## Objetivo

Validar empiricamente construtos e métricas para avaliar e melhorar a transparência em produtos do processo de engenharia de software, especialmente especificações de requisitos de software (SRS). O artigo também propõe um modelo de avaliação e melhoria da transparência baseado em GQM.

## Problema investigado

A transparência é tratada como requisito não funcional emergente, mas ainda não havia medição adequada para transparência no processo de engenharia de software. Sem medidas, ficam indefinidos os fatores que caracterizam transparência, suas relações e seus efeitos sobre manutenibilidade, comunicação e produtividade dos stakeholders.

## Método

- Tipo de estudo: estudo quantitativo com experimento controlado, desenho between-subjects.
- Dados/amostra: 273 respostas coletadas; 252 válidas após triagem. A amostra incluiu profissionais de ICT, estudantes de pós-graduação e um grupo menor de estudantes de graduação/terceiro ano. O dataset foi disponibilizado no IEEE Dataport.
- Procedimento: participantes receberam aleatoriamente uma SRS em linguagem natural (NL-SRS, 39 páginas) ou uma SRS orientada a objetos baseada em modelo de casos de uso (UCM-SRS, 17 páginas). Eles executaram tarefas de usabilidade, reuso, entendimento e análise de impacto, além de responder a questionários.
- Métricas/modelos/instrumentos: paradigma Goal Question Metric (GQM); construtos de acessibilidade, usabilidade, compreensibilidade, modificabilidade e reusabilidade; métricas de tempo, efetividade, eficiência, completude, facilidade de encontrar informação, concisão, legibilidade, conectividade, documentação e percepção dos participantes.
- Técnicas estatísticas: análise no IBM SPSS 28.0.1; transformação de itens Likert em valores numéricos agregados; análise de poder e tamanho de efeito; testes de confiabilidade com alfa de Cronbach; correlações, intercorrelações e regressão múltipla para verificar relações entre construtos, métricas e transparência geral.

## Principais resultados

- Resultado 1: a SRS baseada em casos de uso/orientação a objetos foi mais transparente na prática: os participantes tiveram mais facilidade de manutenção, entendimento e análise de impacto do que na SRS em linguagem natural.
- Resultado 2: o uso de modelagem de casos de uso favoreceu comunicação mais efetiva e eficiente, além de maior produtividade dos participantes, especialmente pelas métricas baseadas em tempo, efetividade e eficiência.
- Resultado 3: os construtos de transparência apresentaram correlações positivas e significativas entre si e com transparência geral. As métricas avaliadas, com exceções ligadas a variáveis de tempo, mediram de modo aceitável os construtos que pretendiam medir.

## Contribuições

O artigo oferece evidência empírica para um conjunto de construtos e métricas de transparência em engenharia de software. Também propõe um modelo prático de melhoria com etapas para estabelecer requisitos de transparência, definir objetivos, selecionar fatores e métricas, executar tarefas de avaliação, analisar resultados, gerar feedback e reavaliar artefatos. A contribuição prática é mostrar que transparência pode ser diagnosticada e melhorada ainda nas fases de requisitos e design.

## Limitações

Os resultados se concentram na fase de engenharia de requisitos e em artefatos SRS, não em todo o ciclo de vida de software. A amostra foi composta principalmente por profissionais de ICT e estudantes com conhecimento técnico, excluindo clientes, usuários finais e stakeholders não técnicos. Os materiais experimentais e tarefas podem não representar toda a variedade de tamanho, complexidade, consistência e rastreabilidade de SRS reais.

## Relação com a disciplina

- Medição: define construtos, métricas e instrumentos para medir transparência como atributo de qualidade em artefatos de software.
- Análise de Medições: usa confiabilidade, correlações, regressão e análise de efeito para avaliar se as métricas realmente representam os construtos.
- Experimentação: aplica experimento controlado com tratamentos distintos (NL-SRS e UCM-SRS), tarefas, hipóteses e análise estatística dos resultados.

## Potencial para o trabalho final

O artigo é útil para um trabalho final sobre medição de atributos não funcionais em artefatos de requisitos. Ele pode fundamentar uma proposta de checklist ou modelo de medição para avaliar transparência, manutenibilidade e comunicação em SRS reais ou em documentos produzidos por equipes de desenvolvimento.

## Citação curta

Ofem, Isong e Lugayizi (2024) mostram que métricas de transparência podem apoiar a avaliação e melhoria de SRS, e que especificações baseadas em casos de uso tendem a favorecer manutenibilidade, comunicação e produtividade.
