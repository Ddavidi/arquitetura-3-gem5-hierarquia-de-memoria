# Análise de Resultados - Simulação de Hierarquia de Cache (gem5)

Este documento foi gerado para auxiliar na escrita do artigo final (etapa 4). Ele contém as observações e análises baseadas nos dados coletados a partir de 16 cenários de simulação da carga de trabalho *PolyBench (gemm)*, variando o tamanho da L1 Data Cache (8kB a 64kB) e a presença de caches L2 e L3.

## 1. Desempenho (IPC e CPI) vs Tamanho da L1D

**Observação dos Dados:**
* Há um ganho notável de IPC (salto de desempenho) ao aumentar a L1D de 8kB para 16kB e, posteriormente, de 16kB para 32kB.
* Quando a L1D aumenta de 32kB para 64kB, o IPC e o Tempo de Execução praticamente se mantêm constantes.
* **Paradoxo da Hierarquia:** A configuração "Apenas L1" apresentou o **melhor desempenho geral** (menor Tempo de Execução, variando de 59.2s a 49.6s, e maior IPC). Ao adicionar a cache L2, o tempo subiu (para a faixa de 61.4s a 56.0s). Quando a L3 foi adicionada, o tempo subiu ainda mais (chegando a 76.8s a 73.0s).

**Discussão para o Artigo:**
O aumento da cache L1D até 32kB é benéfico pois consegue abarcar o *working set* (conjunto de trabalho) das matrizes do programa *gemm*, reduzindo as faltas de capacidade e conflito. O *plateau* (platô) atingido em 64kB indica que a aplicação já não sofre com tantas falhas, não compensando investir em L1 ainda maiores para esta aplicação específica.
O fenômeno em que adicionar mais níveis de cache piora o desempenho pode ser explicado por características do simulador gem5 e da aplicação: As caches L2 e L3 introduzem **latências adicionais de acesso e roteamento em barramentos subjacentes**. Como as matrizes não têm reuso temporal suficiente após caírem da L1 para aproveitar a L2/L3 adequadamente, as requisições pagam a penalidade de verificar a L2/L3 (que geram falta) antes de finalmente buscarem na Memória Principal. Em outras palavras, a latência de *Cache Miss* fica substancialmente maior.

## 2. Taxa de Falha L1D e MPKI vs Tamanho da L1D

**Observação dos Dados:**
* A Taxa de Falha (*Miss Rate*) da L1D e o MPKI (*Misses Per Kilo Instructions*) são ignorantes à presença de caches L2 e L3. Em todos os cenários, um L1D de tamanho igual obteve a mesma taxa de falhas.
* 8kB: ~6.28% (MPKI 31.28)
* 16kB: ~3.81% (MPKI 18.98)
* 32kB: ~3.14% (MPKI 15.65)
* 64kB: ~3.13% (MPKI 15.62)

**Discussão para o Artigo:**
Os gráficos de Miss Rate e MPKI comprovam matematicamente o que foi observado no IPC. O ponto de inflexão ocorre perto dos 32kB. O ganho marginal de investir em 64kB em vez de 32kB é menor do que 0.01% na taxa de falha.
Além disso, o fato das métricas se manterem exatas (L1D independente da topologia geral) prova a consistência e o isolamento arquitetural correto da simulação: Caches mais baixas na hierarquia não afetam o número de acessos e faltas que ocorrem no topo.

## Conclusões Gerais (Dicas para o Texto Final)
* **Recomendação de Arquitetura:** Para a aplicação de multiplicação de matrizes (*gemm*), no modelo abordado, o "sweet spot" (ponto de equilíbrio ótimo) de custo-benefício é uma L1D de 32kB.
* **Trade-offs:** Demonstrar na discussão que "mais cache nem sempre é sinônimo de mais desempenho", pois a latência de interconexão sobrepõe os eventuais ganhos de taxa de acerto em hierarquias complexas caso a carga de trabalho não seja otimizada para tirar proveito da temporalidade em grandes volumes de cache.

---
*Os gráficos (PNGs) baseados nesta análise encontram-se no diretório `results_figs/`. O arquivo `results_figs/dados_compilados.csv` fornece a tabela completa caso precise formatar no LaTex/Word.*
