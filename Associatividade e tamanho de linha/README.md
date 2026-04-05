# Projeto Arquitetura de Computadores III: Analise de Cache com gem5

Este repositorio contem os scripts de configuracao e carga de trabalho (PolyBench/C) para a execucao do trabalho pratico de AC III, simulando o impacto da Associatividade e do Tamanho de Linha de Cache no desempenho do processador.

## Estrutura do Repositorio

* `polybench/`: Codigo-fonte da suite de testes PolyBench/C 4.2.1.
* `gemm`: Executavel gerado estaticamente do programa *gemm* (Multiplicacao de Matrizes com MEDIUM_DATASET), que serve como nosso "Workload".
* `hello`: Executavel de teste simples utilizado para validar o ambiente de simulacao.
* `config.py`: Arquivo de configuracao Python do **gem5**. Parametriza os principais aspectos da hierarquia de cache, permitindo variar associatividade, tamanho de linha, politica de substituicao e politica de escrita via argumentos de linha de comando.
* `resultados/`: Diretorio persistente onde o gem5 armazena as saidas. Cada pasta corresponde a um cenario arquitetural simulado.

## O Que Foi Parametrizado (`config.py`)

Para a exploracao metodologica (onde varia-se apenas um parametro por experimento), o `config.py` recebeu os seguintes argumentos:

* `--assoc`: Associatividade da cache L1 de dados (Ex: `1`, `4`, `8`, `16`).
* `--line_size`: Tamanho da linha de cache em bytes (Ex: `32`, `64`, `128`, `256`).
* `--repl`: Politica de substituicao da cache L1 (opcoes: `LRU`, `Random`, `FIFO`, `LFU`).
* `--write_policy`: Politica de escrita da cache L1 (opcoes: `wb` para write-back, `wt` para write-through).
* `--cmd`: Caminho do binario a ser executado na simulacao.

## Configuracao Fixa do Sistema

Os seguintes parametros foram mantidos constantes em todas as simulacoes:

| Componente | Configuracao |
|---|---|
| CPU | X86TimingSimpleCPU |
| Frequencia | 1 GHz |
| Cache L1 Instrucoes | 32KB, 4-way, LRU |
| Cache L1 Dados | 64KB (tamanho fixo) |
| Cache L2 | 256KB, 8-way, LRU |
| Memoria RAM | 512MB DDR3-1600 |
| Workload | PolyBench/C gemm MEDIUM_DATASET |

## Baterias de Simulacao

### Bateria 1 - Associatividade
Variando a associatividade da L1, mantendo `line_size=64`, `repl=LRU`, `write_policy=wb`:

| Simulacao | Associatividade | Miss Rate L1 | IPC |
|---|---|---|---|
| assoc_1 | 1-way (direct mapped) | 0.6986% | 0.2591 |
| assoc_4 | 4-way | 0.6017% | 0.2600 |
| assoc_16 | 16-way | 0.6017% | 0.2600 |

### Bateria 2 - Tamanho de Linha
Variando o tamanho da linha de cache, mantendo `assoc=4`, `repl=LRU`, `write_policy=wb`:

| Simulacao | Tamanho de Linha | Miss Rate L1 | IPC |
|---|---|---|---|
| line_32 | 32 bytes | 1.2031% | 0.2427 |
| line_64 | 64 bytes | 0.6017% | 0.2600 |
| line_256 | 256 bytes | 0.1505% | 0.2715 |

## Como Reproduzir

### Pre-requisitos

* Docker Desktop instalado e rodando
* Repositorio gem5 clonado em `~/gem5/`
* gem5 compilado via Docker (`build/ALL/gem5.opt`)

### 1. Compilar o workload

```bash
docker run --rm -v ~/gem5:/gem5 \
  ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0 \
  /bin/bash -c "gcc -O0 -static \
    -I /gem5/polybench/utilities \
    -I /gem5/polybench/linear-algebra/blas/gemm \
    -DMEDIUM_DATASET \
    /gem5/polybench/utilities/polybench.c \
    /gem5/polybench/linear-algebra/blas/gemm/gemm.c \
    -o /gem5/gemm"
```

### 2. Rodar uma simulacao

```bash
docker run --rm -v ~/gem5:/gem5 \
  ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0 \
  /bin/bash -c "cd /gem5 && build/ALL/gem5.opt -d resultados/NOME_DA_PASTA config.py \
    --assoc=4 --line_size=64 --repl=LRU --write_policy=wb --cmd=/gem5/gemm"
```

### 3. Rodar simulacoes em paralelo

Abra multiplos terminais e rode um comando por terminal, alterando apenas o parametro de interesse e o nome da pasta de saida (`-d`). Cada container e independente e salva seus resultados em pastas separadas.

## Analisando as Metricas

Apos a simulacao finalizar, os resultados ficam em `~/gem5/resultados/NOME_DA_PASTA/stats.txt`.

Linhas-chave para analise:

* **IPC:** `system.cpu.ipc` - instrucoes por ciclo (maior e melhor).
* **Miss Rate L1:** `system.cpu.dcache.overallMissRate::total` - taxa de falha da cache L1 (0 a 1).
* **Misses absolutos L1:** `system.cpu.dcache.overallMisses::total`.
* **Instrucoes simuladas:** `simInsts` - base para calculo do MPKI.
* **Ticks simulados:** `simTicks` - tempo total de simulacao.

### Calculo do MPKI

```
MPKI = overallMisses::total / (simInsts / 1000)
```

### Comandos uteis para extrair metricas

```bash
# Miss rate L1
grep "dcache.overallMissRate::total" ~/gem5/resultados/PASTA/stats.txt

# IPC
grep "system.cpu.ipc" ~/gem5/resultados/PASTA/stats.txt

# Misses absolutos e instrucoes
grep -E "overallMisses::total|simInsts" ~/gem5/resultados/PASTA/stats.txt
```
