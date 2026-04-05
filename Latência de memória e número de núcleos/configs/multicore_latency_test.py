import sys
import os
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.simple import SingleChannelSimpleMemory
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource, BinaryResource
from gem5.simulate.simulator import Simulator

# --- CAPTURA DE PARÂMETROS ---
# O script espera o número de núcleos e a latência de memória como argumentos
# Exemplo: gem5.opt script.py 4 50ns
n_cores = int(sys.argv[1]) if len(sys.argv) > 1 else 1
mem_latency_ns = sys.argv[2] if len(sys.argv) > 2 else "30ns"

print(f"--- Configurando Simulação Arquitetural ---")
print(f"Número de Núcleos (Cores): {n_cores}")
print(f"Latência de Memória: {mem_latency_ns}")
print(f"Workload: Polybench GEMM (Aceleração de Álgebra Linear)")
print(f"Objetivo: Analisar latência de memória e escalabilidade de núcleos no gemm")

# 1. Hierarquia de Cache (L1 e L2 Privadas)
# Definimos tamanhos padrão para L1 (Instruções e Dados) e L2
# Para este trabalho, focaremos na variação de núcleos e latência de memória
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1i_size="32KiB",
    l1d_size="32KiB",
    l2_size="256KiB"
)

# 2. Sistema de Memória
# Simulando uma memória simples para testar a latência parametrizada
memory = SingleChannelSimpleMemory(
    latency=mem_latency_ns,
    latency_var="0ns",
    bandwidth="12.8GiB/s",
    size="1GiB"
)

# 3. Processador (Modelo de CPU de Tempo/Timing)
# O TimingSimpleCPU é essencial para medir o tempo de execução e latência reais
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, 
    isa=ISA.X86, 
    num_cores=n_cores
)

# 4. Montagem da Placa (SimpleBoard)
# Integra CPU, Memória e Cache em um sistema completo
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# 5. Definição do Workload (Polybench GEMM)
# Tenta carregar o binário compilado pelo script setup_polybench.sh
gemm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workloads", "polybench-c", "linear-algebra", "blas", "gemm", "gemm_static")

if os.path.exists(gemm_path):
    print(f"Carregando binário GEMM local para {n_cores} núcleo(s): {gemm_path}")
    if n_cores > 1:
        binaries = [BinaryResource(local_path=gemm_path) for _ in range(n_cores)]
        board.set_se_multi_binary_workload(binaries=binaries)
    else:
        board.set_se_binary_workload(BinaryResource(local_path=gemm_path))
else:
    print(f"AVISO: Binário GEMM não encontrado em {gemm_path}.")
    print("Execute './setup_polybench.sh' na raiz para baixar e compilar.")
    print("Tentando usar recurso padrão de fallback (x86-hello64-static)...")
    board.set_se_binary_workload(obtain_resource("x86-hello64-static"))

# 6. Execução do Simulador
simulator = Simulator(board=board)

print(f"Iniciando simulação... Isso pode levar alguns minutos.")
simulator.run()

print(f"--- Simulação Concluída ---")
print(f"Verifique os resultados na pasta de saída (m5out ou especificada por -d)")