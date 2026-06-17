# Resumo

## Identificação
- Título: The Effects of Change Decomposition on Code Review - A Controlled Experiment
- Aluno: Lucca Oliveira Vasconcelos de Faria
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2019
- Fonte / Evento / Periódico: PeerJ Computer Science, 5:e193
- DOI / URL: DOI 10.7717/peerj-cs.193; https://arxiv.org/abs/1805.10978

## Objetivo

Medir quantitativa e qualitativamente se decompor mudanças de código em pull requests menores e internamente coerentes melhora o processo de revisão de código em comparação com revisar uma mudança emaranhada que mistura conceitos diferentes.

## Problema investigado

O estudo investiga se mudanças emaranhadas aumentam a carga cognitiva dos revisores, levando a mais falsos positivos, perda de defeitos, maior tempo de revisão, pior compreensão da intenção da mudança ou padrões de navegação menos eficientes durante modern code review.

## Método
- Tipo de estudo: Experimento controlado assíncrono com análise quantitativa e qualitativa.
- Dados / amostra: 28 participantes, incluindo desenvolvedores profissionais, estudantes de doutorado e estudantes de mestrado, divididos em grupo controle com pull request emaranhado e grupo tratamento com mudanças decompostas.
- Procedimento: Os participantes revisaram mudanças no sistema Java open-source JPacman, envolvendo uma nova funcionalidade de inteligência artificial de inimigo e uma refatoração em classes de inimigos. O grupo controle recebeu uma mudança combinada; o grupo tratamento recebeu duas mudanças separadas. O ambiente usou GitHub, Eclipse em máquina virtual, screencasts e monitoramento com WatchDog.
- Métricas, modelos ou instrumentos utilizados: Número de defeitos encontrados, falsos positivos, melhorias sugeridas, tempo líquido de revisão, tempo até identificar defeitos, questionário pós-experimento em escala Likert sobre compreensão e percepção da mudança, além de padrões qualitativos extraídos dos screencasts.
- Técnicas estatísticas, quando houver: Testes Mann-Whitney U para comparar grupos, nível de confiança de 95%, Cliff's delta para tamanho de efeito em falsos positivos e análise qualitativa por codificação dedutiva inspirada em análise de conteúdo.

## Principais resultados
- Resultado 1: Pull requests decompostos geraram menos falsos positivos de forma estatisticamente significativa; o efeito reportado foi médio, com Cliff's delta de 0,36.
- Resultado 2: Não houve evidência estatística de diferença no número de defeitos encontrados, no número de melhorias sugeridas, no tempo líquido de revisão ou no tempo de vida dos defeitos.
- Resultado 3: A decomposição não melhorou de forma mensurável a compreensão declarada da rationale da mudança, mas os participantes reconheceram que as mudanças decompostas eram mais bem separadas, melhor estruturadas e menos espalhadas por múltiplas funcionalidades.

## Contribuições

O artigo oferece evidência experimental de que decompor mudanças pode reduzir ruído na revisão, especialmente falsos positivos. Também fornece um desenho experimental replicável para estudar code review em ambiente pull-based e caracteriza padrões de navegação, mostrando que revisores de mudanças decompostas tendem a buscar mais contexto em classes relacionadas.

## Limitações

A amostra é pequena e obtida por conveniência. O experimento usou um único sistema Java, um conjunto específico de mudanças, GitHub como plataforma e máquina virtual como ambiente controlado, o que limita generalização. A execução assíncrona reduz controle sobre interferências externas, e o estudo não cobre mudanças maiores, outros domínios, outras linguagens ou contextos industriais completos.

## Relação com a disciplina
Conexão com:
- Medição em Engenharia de Software: Define e coleta medidas operacionais de revisão, como defeitos encontrados, falsos positivos, melhorias sugeridas e tempos de revisão.
- Análise de Medições de Software: Usa comparação estatística não paramétrica e tamanho de efeito para interpretar dados com amostra pequena e possível distribuição assimétrica.
- Experimentação em Engenharia de Software: É um experimento controlado com tratamento, grupo controle, hipóteses, variáveis dependentes, ameaças à validade e análise qualitativa complementar.

## Potencial para o trabalho final

O artigo pode servir como base para um trabalho final sobre qualidade de revisão de código, decomposição de mudanças, métricas de pull requests ou análise experimental de práticas de desenvolvimento. Também oferece variáveis mensuráveis e um desenho replicável para avaliar revisão de código em pequenos grupos.

## Citação curta

Di Biase et al. mostram que decompor mudanças em pull requests coerentes reduz falsos positivos na revisão de código, embora não aumente significativamente defeitos encontrados nem reduza o tempo total de revisão.
