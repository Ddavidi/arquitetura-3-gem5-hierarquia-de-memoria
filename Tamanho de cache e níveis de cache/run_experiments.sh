#!/bin/bash

# Caminhos (AJUSTA SE NECESSÁRIO)
GEM5_BIN=/home/bernardo-eng/gem5/build/X86/gem5.opt
CONFIG_PY=/home/bernardo-eng/projeto_arquitetura/scripts/config.py
PROGRAMA=/home/bernardo-eng/projeto_arquitetura/benchmarks/polybench_gemm_exe

# Variaveis de Analise de Arquitetura
TAMANHOS_L1D=("8kB" "16kB" "32kB" "64kB")
OPCOES_L2=("False" "True")
OPCOES_L3=("False" "True")

# Prepara a pasta de resultados generalizada
mkdir -p results

echo "------------------------------------------------------------------"
echo " Iniciando Bateria Completa de Testes no Gem5"
echo " Cobertura Total: 16 combinacoes cartesianas (L1, L2, L3)"
echo "------------------------------------------------------------------"

for L3 in "${OPCOES_L3[@]}"
do
    for L2 in "${OPCOES_L2[@]}"
    do
        for SIZE in "${TAMANHOS_L1D[@]}"
        do
            echo ""
            echo "================================================="
            echo " [CENARIO] L1D: $SIZE | L2: $L2 | L3: $L3 "
            echo "================================================="
            
            OUT_DIR="results/l1_${SIZE}_l2_${L2}_l3_${L3}"
            
            $GEM5_BIN -d $OUT_DIR $CONFIG_PY \
                --l1d_size=$SIZE \
                --l2_cache=$L2 --l2_size=256kB \
                --l3_cache=$L3 --l3_size=1MB \
                --cmd=$PROGRAMA
        done
    done
done

echo ""
echo "################################################################"
echo "Todos os 16 simuladores finalizaram! "
echo "Visite a pasta results/ e extraia os dados do arquivo stats.txt"
echo "################################################################"
