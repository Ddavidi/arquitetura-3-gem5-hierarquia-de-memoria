#!/bin/bash

# Diretórios de configuração e execução
GEM5_BIN="./gem5/build/X86/gem5.opt"
CONFIG_SCRIPT="./configs/multicore_latency_test.py"
RESULTS_DIR="./results"

# Garante que a pasta de resultados existe
mkdir -p $RESULTS_DIR

echo "--- Iniciando Experimentos de Arquitetura III ---"

# Arrays com os cenários experimentais
CORES=(1 2 4)
LATENCIES=("30ns" "50ns" "100ns")

for core in "${CORES[@]}"
do
    for latency in "${LATENCIES[@]}"
    do
        OUTPUT_DIR="$RESULTS_DIR/${core}_cores_${latency}"
        echo "Executando simulação para $core núcleo(s) e latência $latency..."
        echo "Resultados serão salvos em: $OUTPUT_DIR"
        
        # Execução do gem5 em paralelo processando no background (&)
        # -d define o diretório de saída, e a saída do terminal é salva para não sujar a tela
        $GEM5_BIN -d $OUTPUT_DIR $CONFIG_SCRIPT $core $latency > $OUTPUT_DIR/gem5_console.log 2>&1 &
        
        echo "Disparado em background: $core núcleo(s) e latência $latency."
        echo "------------------------------------------------"
    done
done

echo "Aguardando a finalização de todas as simulações simultâneas... (Isso usa bastante CPU)"
wait

echo "Todos os experimentos em paralelo foram concluídos!"
echo "Verifique a pasta $RESULTS_DIR para as métricas (stats.txt)."