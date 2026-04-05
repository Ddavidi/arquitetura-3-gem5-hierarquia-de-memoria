# Análise de Resultados e Discussão de Hardware

Este documento fornece a análise detalhada dos testes do **GEMM (Polybench)** executados no simulador gem5, variando contagens de núcleos (1, 2, 4 cores) e a latência de acesso à memória (30ns, 50ns, 100ns). Esta análise leva como premissa o modelo de carga de trabalho **multiprogramada** (*multi-programmed workload*), onde cada núcleo da CPU executa uma instância isolada e simultânea do benchmark GEMM.

O objetivo destas análises guiadas é compilar discussões pertinentes que fundamentem **o artigo final do trabalho** (referente à etapa 4).

---

## 1. Tempo de Execução Geral vs. Latência
*(Gráfico referenciado: grafico_tempo_execucao.png)*

**Discussão Analítica:**
Os dados extraídos (`simSeconds`) revelam um fenômeno fascinante sobre a escalabilidade da arquitetura: os tempos de execução se mantiveram quase constantes, na faixa de **~3.9s**, independentemente de estarmos rodando 1, 2 ou 4 núcleos na configuração de menor latência (30ns e 50ns).

No modelo multiprogramado, uma configuração de 4 núcleos (que termina em ~3.97s) executou **4 vezes mais cálculos** (quatro instâncias inteiras do GEMM) no mesmo intervalo de tempo que a configuração de 1 núcleo (que terminou em ~3.89s). Esse comportamento certifica níveis excelentes de **Throughput (Vazão)** no processador em cenários de baixo acoplamento/compartilhamento de dados inter-threads. A arquitetura forneceu largura de banda e isolamento de cache suficientes para sustentar múltiplas execuções do algoritmo denso com um custo irrisório de *overhead* e contenção entre os núcleos nas latências de até 50ns.

Por outro lado, o impacto exclusivo da latência foi de acordo com a teoria fundamental de arquitetura. O tempo de execução de todas as simulações sobe levemente a 100ns devido às "bolhas" (stalls) inseridas no pipeline de execução, pois processador é forçado a esperar pela memória lenta.

---

## 2. Taxa de Faltas (Miss Rate) na Cache L2 vs. Latência
*(Gráfico referenciado: grafico_l2_miss_rate.png)*

**Discussão Analítica:**
A métrica de acessos faltosos (`overallMissRate`) para a camada L2 traz à tona o verdadeiro custo da alta latência no barramento principal. Em intervalos toleráveis (como 30ns e 50ns), a taxa de falha sofre menos pertubação porque o controlador de cache consegue despachar e acomodar as requisições pendentes. 

No entanto, quando se estipula o limiar de **100ns**, nota-se uma disrupção sistêmica na hierarquia de memória, causando picos substanciais nos Miss Rates. 

**Possíveis interpretações para o artigo:**
Esse súbito engasgamento não resulta apenas do algoritmo, mas do esgotamento mecânico da Cache. Com uma latência excessiva (100ns), as requisições de carga e armazenamento (`Load/Store`) demoram a dar retorno, o que satura os *MSHRs (Miss Status Holding Registers)* do gem5 (estruturas finitas que acomodam os acessos ocorrendo na memória). Com os registradores lotados, as novas requisições vindas dos cálculos de matrizes sequer podem ser acomodadas e viram faltas compulsórias, ou pior, geram estrangulamento do fluxo prefetcher. É um excelente exemplo empírico do que a literatura chama de *"The Memory Wall"* (O Gargalo da Memória).

---
*Fim do Relatório*

