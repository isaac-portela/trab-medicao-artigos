# Resumo

## Identificação

- Título: Medição e Análise no CMMI com Metodologia Seis Sigma e ISO/IEC/IEEE 15939
- Autores: Charles S. F. Silva e Marcelo S. Oliveira
- Ano informado no PDF: 2022
- Ano indicado na pasta e no `info.md`: 2023
- Fonte indicada em `info.md`: https://publicacoes.unifal-mg.edu.br/revistas/index.php/sigmae/article/view/597/1561
- Aluno: Gabriel Ferreira Amaral

## Objetivo

Propor e demonstrar uma forma de conjugar a metodologia Seis Sigma com a estrutura conceitual de medição da norma ISO/IEC/IEEE 15939 para atender às necessidades de medição e análise exigidas pelo CMMI.

## Problema investigado

O CMMI define expectativas para medição e análise, mas não determina qual sistema de medição deve ser usado nem como implementá-lo. O artigo investiga essa lacuna: como construir uma sistemática de medição que ajude a organização a avaliar capacidade versus desempenho do processo e a orientar melhoria contínua.

## Método

O trabalho apresenta uma discussão conceitual sobre CMMI, Seis Sigma e ISO/IEC/IEEE 15939, seguida de um estudo de caso em uma pequena empresa desenvolvedora de software, identificada ficticiamente como XYZ. A empresa usava ciclo de vida iterativo incremental e buscava avançar do nível 1 para o nível 2 de maturidade na representação por estágios do CMMI.

Foram definidas necessidades de informação relacionadas a cronograma, custo e qualidade. As medidas incluíram horas e unidades monetárias estimadas e observadas, diferenças entre valores observados e estimados, e contagem de erros por tipo. Os indicadores foram analisados por correlação, histogramas, gráficos de Pareto e interpretação estatística, com uso de R e LibreOffice Calc.

## Principais resultados

O estudo encontrou coeficientes de correlação muito próximos de 1 para estimativas de cronograma e custo: 0,9994 para cronograma e 0,9993 para custo. Isso indicou alta precisão das estimativas no projeto analisado, embora o artigo ressalte que esse resultado é incomum na indústria de software.

Os histogramas das diferenças entre valores observados e estimados apresentaram assimetria à direita, sugerindo presença de causas especiais de variação, associadas principalmente às fases de planejamento e fechamento. Na análise de qualidade, o Pareto mostrou maior concentração de erros de gravidade pequena e de erros relacionados a requisitos funcionais. O artigo recomenda medições futuras e cartas de controle para verificar estabilidade, previsibilidade e oportunidades de melhoria.

## Contribuições

A contribuição central é mostrar um caminho prático para operacionalizar medição e análise no CMMI usando a ISO/IEC/IEEE 15939 como estrutura de medição e o Seis Sigma como orientação quantitativa e estatística. O artigo também exemplifica como transformar necessidades de informação em medidas, indicadores e decisões gerenciais.

## Limitações

O estudo se baseia em um único projeto de uma empresa pequena, com nome fictício, o que limita a generalização dos resultados. Além disso, os próprios autores indicam a necessidade de medições em projetos futuros de categoria similar para confirmar estabilidade dos processos e permitir o uso mais consistente de cartas de controle.

## Relação com a disciplina

O artigo é fortemente ligado à disciplina por tratar de medição de software, indicadores, processo de medição, análise estatística e melhoria de processos. Ele conecta conceitos de medidas básicas, medidas derivadas e indicadores com decisões sobre prazo, custo e qualidade.

## Potencial para o trabalho final

O artigo pode apoiar um trabalho final sobre implantação de um processo de medição alinhado ao CMMI ou à ISO/IEC/IEEE 15939. Também pode servir como exemplo para estruturar indicadores de cronograma, custo e qualidade, incluindo análise de correlação, histograma, Pareto e cartas de controle.

## Citação curta

Silva e Oliveira (2022) demonstram que Seis Sigma e ISO/IEC/IEEE 15939 podem complementar o CMMI ao transformar necessidades de informação em medições, indicadores estatísticos e ações de melhoria de processo.
