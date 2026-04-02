#!/bin/bash
set -e

echo "Baixando Polybench-C 4.2.1..."
cd workloads
if [ -d "polybench-c" ]; then
    echo "Pasta polybench-c já existe. Removendo..."
    rm -rf polybench-c
fi
git clone https://github.com/MatthiasJReisinger/PolyBenchC-4.2.1.git polybench-c

echo "Compilando gemm (com SMALL_DATASET para terminar mais rápido)..."
cd polybench-c/linear-algebra/blas/gemm
# Compilando estaticamente para o gem5 (x86) com dataset reduzido para simulação
gcc -O3 -I ../../../utilities -I . ../../../utilities/polybench.c gemm.c -o gemm_static -static -DPOLYBENCH_TIME -DSMALL_DATASET

echo "Sucesso! O binário gemm_static foi criado."
