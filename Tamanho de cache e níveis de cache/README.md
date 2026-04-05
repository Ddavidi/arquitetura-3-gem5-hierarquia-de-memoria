# Projeto Arquitetura de Computadores III: Análise de Cache com gem5

Este repositório contém os scripts de automação e carga de trabalho (PolyBench) para a execução do trabalho prático de AC III, simulando o impacto do Tamanho de Cache e dos Níveis de Cache.

## Estrutura do Repositório

* `benchmarks/polybench/`: Código-fonte da suíte de testes PolyBench (C).
* `benchmarks/polybench_gemm_exe`: Executável gerado estaticamente do programa *gemm* (Multiplicação de Matrizes), que serve como nosso "Workload".
* `scripts/config.py`: Arquivo de configuração Python do **gem5**. Ele foi refatorado para suportar topologias de memória personalizadas, permitindo habilitar/desabilitar uma Cache L2 dinamicamente, além de parametrizar o tamanho da L1 Data Cache.
* `run_experiments.sh`: Script em Bash que automatiza as baterias de testes, cruzando as opções de Tamanho e Nível de Cache de forma controlada.
* `results/`: Diretório persistente onde o gem5 armazenará as saídas. Cada pasta corresponderá a um cenário arquitetural (ex: `l1_16kB_l2_False`).

## O Que Foi Parâmetrizado (`config.py`)

Para a exploração metodológica (onde varia-se apenas um parâmetro por experimento), o `scripts/config.py` recebeu os seguintes argumentos:
* `--l1d_size`: Tamanho da cache L1 de Dados (Ex: `8kB`, `16kB`, `32kB`, `64kB`).
* `--l2_cache`: Um booleano (`True` ou `False`). Se passado `True`, instancia-se o barramento de ponte L2XBar e a Cache L2.
* `--l2_size`: Tamanho da L2 (ativa caso `--l2_cache=True`).
* `--l3_cache`: Um booleano (`True` ou `False`). Se passado `True`, instancia-se um nível adicional de cache L3 compartilhada.
* `--l3_size`: Tamanho da L3 (ativa caso `--l3_cache=True`).

*Atenção aos Colegas de Equipe:* Demais parâmetros como Associatividade ou Política de Substituição de Cache estão definidos como "Constantes" (*hardcoded*) dentro do código fonte do `config.py`. Para variar o aspecto da associatividade, siga o padrão de código que implementamos e adicione um parser parameter.

## Como Reproduzir

1. Acesse o servidor ou abra o terminal do Linux.
2. Certifique-se de estar na pasta raiz do projeto:
   ```bash
   cd ~/projeto_arquitetura
   ```
3. Conceda permissão de execução ao script (Obrigatório apenas na primeira vez):
   ```bash
   chmod +x run_experiments.sh
   ```
4. Execute os cenários:
   ```bash
   ./run_experiments.sh
   ```

## Analisando as Métricas para o Artigo

Após a simulação finalizar, extraia os arquivos de métricas navegando pelas ramificações do diretório de `results/`.
Para plotar os gráficos, abra o arquivo `stats.txt` específico de cada simulação.

Preste atenção as linhas-chave solicitadas no edital da atividade:
* **CPI/IPC:** Identifique `system.cpu.cpi`. Avalia velocidade geral (menor é melhor para o CPI).
* **Instruções Base:** Identifique `simInsts` (geralmente encontrado nas primeiras 20 linhas).
* **Miss Rate Geral:** Identifique `system.cpu.dcache.overallMissRate::total`. Mostra a taxa de falha (0 a 1).
* **Falhas (Absoluto L1 Data):** `system.cpu.dcache.overallMisses::total`.

*(Dica: Para o cálculo do **MPKI** exigido no enunciado, aplique a fórmula dividindo `overallMisses::total` por `(simInsts / 1000)`).*
