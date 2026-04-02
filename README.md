# Projeto: Arquitetura III - GEM5 Missão Hierarquia de Memória

## Objetivo do Trabalho
O objetivo principal deste trabalho é realizar **experimentos arquiteturais controlados** utilizando o simulador de arquiteturas **gem5**. 

O estudo foca em avaliar o impacto no desempenho de sistema ao variar dois parâmetros cruciais da arquitetura:
- **Latência de Memória** (ex: 30ns, 50ns, 100ns)
- **Número de Núcleos** (ex: 1, 2 e 4 cores)

Para stressar a arquitetura, usamos o workload GEMM (General Matrix Multiply) do benchmark **Polybench**. A fim de garantir uma observação real de concorrência e comportamento de cache, as simulações multicore foram estruturadas sob um modelo de multiprogramação (*multi-programmed workload*), no qual cada núcleo da CPU executa simuntaneamente a sua própria instância do executável.

## Sumário do Repositório

* `configs/`: Scripts de configuração e customização da arquitetura/topologia para o gem5.
* `scripts/`: Ferramentas auxiliares, como o extrator de dados e plotador gráfico (`plot_results.py`).
* `workloads/`: Binários do Polybench compilados para inserção na simulação.
* `results/`: Diretório gerado para acomodar as estatísticas brutas (`stats.txt`) da simulação.
* `ANALISE_RESULTADOS.md` - Um documento contendo a discussão e extração analítica do experimento visando a redação acadêmica (artigos).

## Requisitos Básicos

- `gem5` plenamente compilado e operante no diretório `gem5/build/X86/gem5.opt`
- `python3` com as bibliotecas correspondentes para enxergar os gráficos e dados.
  * *Para instalar usando pip: `pip install matplotlib`*

## Como Reproduzir os Experimentos

O processo inteiro foi automatizado para garantir a confiabilidade e replicabilidade dos testes. Há dois passos primários formados pelo script que orquestra as baterias de testes e pelo script final de plotagem dos resultados gráficos:

### 1. Disparando as Simulações do GEM5
Há um script em Bash cujo papel é varrer as possíveis combinações de núcleos e latências e lançar as instâncias do gem5. Para agilizar o processo longo de simulação da Arquitetura, ele as submete em paralelo no background.
Para executar:
```bash
./run_experiments.sh
```
*(Atenção: O console avisará que todas começaram juntas. Este processo usa muita CPU do computador que está emulando, e você só precisa aguardar que ele lance no terminal que finalizou.)*

### 2. Tratando os Dados e Montando Gráficos
À medida que as simulações encerram, o `gem5` alimentará a pasta de relatórios correspondente em `results/<cores>_cores_<latencia>ns/stats.txt`.
Para juntar esses relatórios volumosos de forma inteligente e extrair apenas a informação relevante (Cache Misses e os simSeconds transcorridos na simulação):
```bash
python3 scripts/plot_results.py
```
Isso varrerá a árvore de resultados, cruzará os dados num gráfico matplotlib, e o despejará como imagens visuais `.png` dentro do caminho `results/graficos`.