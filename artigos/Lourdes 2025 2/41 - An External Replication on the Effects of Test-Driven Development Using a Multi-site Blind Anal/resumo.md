# Resumo

## Identificação
- Título: An External Replication on the Effects of Test-driven Development Using a Multi-site Blind Analysis Approach
- Aluno: Joao Victor Salim Ribeiro Guimaraes Trad
- Grupo: Lourdes 2025/2
- Arquivo: artigo.pdf
- Ano: 2016
- Fonte / Evento / Periódico: ESEM '16 - ACM/IEEE International Symposium on Empirical Software Engineering and Measurement, Ciudad Real, Espanha
- DOI / URL: https://doi.org/10.1145/2961111.2962592

## Objetivo

Validar os resultados de um experimento anterior da Universidade de Oulu sobre os efeitos do Test-Driven Development (TDD), comparando TDD com uma abordagem test-last development (TLD) quanto a esforço de teste, qualidade externa do código e produtividade dos desenvolvedores.

## Problema investigado

O artigo investiga se TDD produz diferenças mensuráveis em relação a TLD em um contexto experimental controlado. A motivação é que estudos anteriores sobre TDD apresentam resultados inconclusivos ou inconsistentes, e a replicação externa é necessária para avaliar a robustez das evidências.

## Método
- Tipo de estudo: Replicação externa próxima de experimento controlado, com desenho crossover balanceado e análise cega multi-site.
- Dados / amostra: 21 estudantes de mestrado em Ciência da Computação da Universidade de Basilicata; 20 observações foram usadas em algumas análises após exclusões/pares completos.
- Procedimento: Os participantes executaram duas tarefas de programação em Java/Eclipse/JUnit, Mars Rover API e Bowling Scorekeeper, aplicando TDD em uma sessão e TLD em outra, em sequências alternadas. A extração dos dados ocorreu em um local e a análise em outro, sem que os analistas conhecessem o objetivo do experimento.
- Métricas, modelos ou instrumentos utilizados: TEST, número de testes escritos; QLTY, qualidade externa medida por suítes de testes de aceitação; PROD, produtividade dos desenvolvedores; tarefas experimentais BSK e MRA.
- Técnicas estatísticas, quando houver: Teste de sinais para diferenças pareadas, teste de Kruskal-Wallis para efeitos de ordem e carryover, tamanho de efeito por Cliff's delta e nível de significância para rejeição das hipóteses nulas.

## Principais resultados
- Resultado 1: Não houve evidência de diferença significativa entre TDD e TLD em esforço de teste, qualidade externa ou produtividade; os resultados principais reportados no resumo foram p = .27, p = .82 e p = .83.
- Resultado 2: Os tamanhos de efeito foram negligenciáveis, reforçando a conclusão de que a replicação confirma o experimento-base de Oulu em contexto acadêmico semelhante.
- Resultado 3: Houve evidência de efeito de ordem entre as sequências de aplicação dos tratamentos, mas os testes não indicaram carryover significativo; os autores suspeitam de interação entre tarefa experimental e tratamento.

## Contribuições

O estudo fortalece a evidência empírica sobre TDD ao replicar externamente um experimento anterior com desenho diferente. Também contribui metodologicamente ao demonstrar uma estratégia de análise cega multi-site para reduzir viés dos pesquisadores e ao discutir a importância da escolha das tarefas em experimentos de Engenharia de Software.

## Limitações

As principais limitações são o uso de estudantes como participantes, a amostragem por conveniência, o contexto acadêmico, a medição de cada variável dependente por uma única métrica e a possibilidade de que as tarefas experimentais interajam com a ordem dos tratamentos. A generalização para profissionais e projetos reais deve ser feita com cautela.

## Relação com a disciplina
Conexão com:
- Medição em Engenharia de Software: O artigo operacionaliza constructos como esforço de teste, qualidade externa e produtividade em métricas mensuráveis e comparáveis.
- Análise de Medições de Software: O estudo usa análise estatística não paramétrica, tamanho de efeito e comparação de distribuições para interpretar medições experimentais.
- Experimentação em Engenharia de Software: É um exemplo direto de replicação externa, desenho crossover, controle de ameaças à validade e análise cega em experimento de Engenharia de Software.

## Potencial para o trabalho final

O artigo pode apoiar um trabalho final sobre avaliação empírica de práticas ágeis, desenho de experimentos controlados, replicação em Engenharia de Software ou influência das métricas e tarefas experimentais na interpretação de resultados. Também é útil como referência metodológica para discutir validade interna, externa, de constructo e de conclusão.

## Citação curta

Fucci et al. (2016) replicam externamente um experimento sobre TDD e não encontram evidência de vantagem significativa de TDD sobre TLD em esforço de teste, qualidade externa ou produtividade, embora observem efeitos relacionados à ordem das tarefas.
