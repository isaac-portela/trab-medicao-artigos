# Resumo

## Identificação

- Título: LLM4DS: Evaluating Large Language Models for Data Science Code Generation
- Autores: Nathalia Nascimento, Everton Guimaraes, Sai Sanjna Chintakunta e Santhosh Anitha Boominathan
- Ano: 2024
- Fonte: arXiv:2411.11908
- Aluno: Emmanuel Viglioni
- Link original: https://arxiv.org/abs/2411.11908

## Objetivo

Avaliar empiricamente a capacidade de assistentes baseados em grandes modelos de linguagem para gerar código Python em tarefas de ciência de dados. O artigo compara Microsoft Copilot, ChatGPT, Claude e Perplexity Labs em problemas de manipulação, algoritmos e visualização de dados.

## Problema investigado

Apesar do uso crescente de LLMs para programação, ainda há pouca evidência específica sobre seu desempenho em ciência de dados. Benchmarks gerais de programação não capturam bem tarefas com bibliotecas, dados tabulares, visualizações e restrições de plataformas de análise. O estudo investiga se esses modelos resolvem problemas de ciência de dados acima de linhas de base estatísticas e se desempenho varia por dificuldade, tipo de tarefa, tempo de execução e qualidade visual.

## Método

O trabalho usa um experimento controlado guiado por Goal-Question-Metric (GQM). Foram selecionados 100 problemas Python da plataforma Stratascratch, distribuídos por três tipos de tarefa: Analytical, Algorithm e Visualization; e por três níveis de dificuldade: easy, medium e hard. Cada problema foi submetido a quatro assistentes: Microsoft Copilot (GPT-4 Turbo), ChatGPT (o1-preview), Claude (3.5 Sonnet) e Perplexity Labs (Llama-3.1-70b-instruct), totalizando 400 soluções.

Os pesquisadores criaram templates de prompt por tipo de tarefa, executaram as soluções na Stratascratch e registraram sucesso, tempo de execução para tarefas analíticas e similaridade dos gráficos para tarefas de visualização. A análise incluiu testes binomiais para linhas de base de 50%, 60% e 70%, testes de Friedman/Wilcoxon para comparações pareadas, qui-quadrado para tipo de tarefa e testes não paramétricos para eficiência e similaridade.

## Principais resultados

Todos os modelos superaram significativamente a linha de base de 50% de sucesso. As taxas gerais foram: ChatGPT 72%, Claude 70%, Perplexity 66% e Copilot 60%. Na linha de base de 60%, apenas ChatGPT e Claude tiveram resultado estatisticamente significativo; nenhum modelo superou significativamente a linha de base de 70%.

O ChatGPT apresentou o desempenho mais consistente entre níveis de dificuldade, enquanto Claude e Perplexity variaram mais conforme a complexidade. O tipo de tarefa, de forma geral, não teve impacto estatisticamente significativo nas taxas de sucesso. Em tarefas analíticas, não houve diferença estatística relevante no tempo de execução, embora o ChatGPT tenha tendido a ser mais lento e menos previsível. Em visualização, as diferenças de similaridade também não foram estatisticamente significativas, mas o ChatGPT obteve a média mais alta e resultados mais consistentes.

## Contribuições

O artigo contribui com uma avaliação empírica específica para geração de código em ciência de dados, área menos coberta por benchmarks gerais. Também propõe uma estrutura experimental com perguntas, hipóteses, métricas e templates de prompt, além de avaliar a Stratascratch como fonte de problemas para estudos de LLMs. Os resultados ajudam a orientar a escolha de modelos conforme confiabilidade, dificuldade e tipo de tarefa.

## Limitações

As principais ameaças à validade envolvem possível presença de problemas semelhantes nos dados de treinamento dos modelos, influência do desenho dos prompts, uso de apenas 100 problemas de uma única plataforma e possibilidade de subjetividade nas pequenas edições manuais permitidas para adequar código às restrições da Stratascratch. O estudo também não avalia formalmente a experiência dos pesquisadores que interagiram com os modelos e executaram as soluções.

## Relação com a disciplina

O artigo se relaciona diretamente com experimentação em Engenharia de Software por formular questões de pesquisa, hipóteses, variáveis independentes e dependentes, métricas e ameaças à validade. Ele exemplifica como comparar tecnologias de apoio ao desenvolvimento usando desenho experimental, testes estatísticos e interpretação cuidadosa de resultados.

## Potencial para o trabalho final

O artigo pode apoiar um trabalho final sobre avaliação de ferramentas de IA para desenvolvimento, especialmente se o foco for produtividade, qualidade de código ou confiabilidade em tarefas específicas. Também pode servir como modelo metodológico para construir um experimento próprio com prompts, datasets controlados, métricas de sucesso e análise estatística.

## Citação curta

Nascimento et al. (2024) mostram que LLMs já resolvem parte relevante de tarefas de ciência de dados, mas seu desempenho ainda não é suficientemente confiável para padrões mais exigentes sem avaliação sistemática.
