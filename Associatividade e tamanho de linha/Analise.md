# Analise de Resultados - Simulacao de Hierarquia de Cache (gem5)

Este documento foi gerado para auxiliar na escrita do artigo final (etapa 4). Ele contem as observacoes e analises baseadas nos dados coletados a partir de 6 cenarios de simulacao da carga de trabalho *PolyBench (gemm)*, variando a Associatividade da L1 Data Cache (1-way a 16-way) e o Tamanho de Linha de Cache (32 a 256 bytes).

## 1. Desempenho (IPC) e Taxa de Falha vs Associatividade

**Observacao dos Dados:**
* Ha um ganho notavel de IPC ao aumentar a associatividade de 1-way (direct mapped) para 4-way.
* Quando a associatividade aumenta de 4-way para 16-way, o IPC e o Miss Rate se mantem praticamente constantes.
* 1-way: Miss Rate 0.6986%, IPC 0.2591
* 4-way: Miss Rate 0.6017%, IPC 0.2600
* 16-way: Miss Rate 0.6017%, IPC 0.2600

**Discussao para o Artigo:**
O ganho de desempenho ao aumentar de 1-way para 4-way e explicado pela reducao de conflitos de mapeamento. Em caches de mapeamento direto (1-way), dois enderecos que mapeiam para o mesmo conjunto competem diretamente, forcando substituicoes desnecessarias — as chamadas *falhas de conflito*. Com 4-way, o conjunto possui quatro posicoes, eliminando grande parte dessas colisoes.

O plateau atingido em 4-way indica que a aplicacao *gemm*, com seu padrao de acesso sequencial as matrizes, ja nao sofre com falhas de conflito significativas a partir deste ponto. Aumentar para 16-way nao traz beneficio mensuravel, pois os conflitos residuais ja foram eliminados com 4 vias. Este comportamento e esperado em aplicacoes com boa localidade espacial: ha um ponto de saturacao da associatividade, alem do qual o custo adicional de hardware nao se justifica pelo ganho de desempenho.

## 2. Desempenho (IPC) e Taxa de Falha vs Tamanho de Linha

**Observacao dos Dados:**
* O Tamanho de Linha apresentou impacto muito mais expressivo no desempenho do que a Associatividade.
* Ha uma reducao progressiva e significativa do Miss Rate conforme o tamanho de linha aumenta.
* 32 bytes: Miss Rate 1.2031%, IPC 0.2427
* 64 bytes: Miss Rate 0.6017%, IPC 0.2600
* 256 bytes: Miss Rate 0.1505%, IPC 0.2715

Os graficos de Miss Rate e IPC comprovam matematicamente o impacto da localidade espacial. O *gemm* acessa as matrizes de forma sequencial — elemento por elemento — o que significa que ao carregar uma linha de cache maior, mais elementos adjacentes uteis sao trazidos de uma unica vez, reduzindo drasticamente a necessidade de novas buscas a memoria.

**Discussao para o Artigo:**
A reducao de 8x no Miss Rate ao passar de 32 para 256 bytes de linha demonstra a forte localidade espacial do *gemm*. Linhas maiores funcionam como um *prefetch* implicito: ao buscar um elemento, trazem consigo os proximos elementos que serao acessados em sequencia.

E importante notar, porem, que este beneficio e especifico do padrao de acesso da aplicacao. Em aplicacoes com acesso aleatorio a memoria, linhas de cache maiores poderiam *piorar* o desempenho, pois carregariam dados adjacentes que nunca seriam utilizados — fenomeno conhecido como *cache pollution*. O *gemm*, por sua natureza de multiplicacao de matrizes com loops aninhados e acesso sequencial, e um caso ideal para se beneficiar de linhas de cache maiores.

A reducao do tempo total de simulacao (de 1.935T ticks para 1.730T ticks) ao aumentar o tamanho de linha reforça que menos falhas de cache resultam em menos ciclos de espera por dados da memoria principal, melhorando diretamente o IPC da CPU.

---
*Os graficos baseados nesta analise encontram-se no diretorio `resultados/`. Os arquivos `stats.txt` de cada cenario fornecem a tabela completa de metricas caso necessite formatar no LaTeX/Word.*
