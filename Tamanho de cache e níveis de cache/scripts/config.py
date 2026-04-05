import m5
from m5.objects import *
import sys
import argparse

parser = argparse.ArgumentParser()
# Parametros escolhidos para variacao
parser.add_argument("--l1d_size", type=str, default="64kB")
parser.add_argument("--l2_size", type=str, default="256kB")
parser.add_argument("--l2_cache", type=lambda x: (str(x).lower() == 'true'), default=False)
parser.add_argument("--l3_size", type=str, default="1MB")
parser.add_argument("--l3_cache", type=lambda x: (str(x).lower() == 'true'), default=False)

# Parametros mantidos constantes (podem ser variados depois)
parser.add_argument("--l1i_size", type=str, default="32kB")
parser.add_argument("--cmd", type=str, required=True)
args = parser.parse_args()

# Configuracao Base do Sistema
system = System()
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU Simples por tempo
system.cpu = TimingSimpleCPU()

# ---------- Caches L1 ----------
system.cpu.icache = Cache(size=args.l1i_size, assoc=2, tag_latency=2, data_latency=2, response_latency=2, mshrs=4, tgts_per_mshr=20)
system.cpu.dcache = Cache(size=args.l1d_size, assoc=2, tag_latency=2, data_latency=2, response_latency=2, mshrs=4, tgts_per_mshr=20)

system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

system.membus = SystemXBar()

# Interrupcoes
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports

# ---------- Topologia de Niveis de Cache ----------
if args.l2_cache and not args.l3_cache:
    # L1 + L2
    system.l2bus = L2XBar()
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
    system.l2cache = Cache(size=args.l2_size, assoc=8, tag_latency=20, data_latency=20, response_latency=20, mshrs=20, tgts_per_mshr=12)
    system.l2cache.cpu_side = system.l2bus.mem_side_ports
    system.l2cache.mem_side = system.membus.cpu_side_ports
elif not args.l2_cache and args.l3_cache:
    # L1 + L3 (Sem L2)
    system.l3bus = L2XBar()
    system.cpu.icache.mem_side = system.l3bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l3bus.cpu_side_ports
    system.l3cache = Cache(size=args.l3_size, assoc=16, tag_latency=50, data_latency=50, response_latency=50, mshrs=20, tgts_per_mshr=12)
    system.l3cache.cpu_side = system.l3bus.mem_side_ports
    system.l3cache.mem_side = system.membus.cpu_side_ports
elif args.l2_cache and args.l3_cache:
    # L1 + L2 + L3
    system.l2bus = L2XBar()
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
    system.l2cache = Cache(size=args.l2_size, assoc=8, tag_latency=20, data_latency=20, response_latency=20, mshrs=20, tgts_per_mshr=12)
    system.l2cache.cpu_side = system.l2bus.mem_side_ports
    
    system.l3bus = L2XBar()
    system.l2cache.mem_side = system.l3bus.cpu_side_ports
    system.l3cache = Cache(size=args.l3_size, assoc=16, tag_latency=50, data_latency=50, response_latency=50, mshrs=20, tgts_per_mshr=12)
    system.l3cache.cpu_side = system.l3bus.mem_side_ports
    system.l3cache.mem_side = system.membus.cpu_side_ports
else:
    # Direto na Memoria (Apenas L1)
    system.cpu.icache.mem_side = system.membus.cpu_side_ports
    system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.system_port = system.membus.cpu_side_ports

# ---------- Controlador de Memoria RAM ----------
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# ---------- Inicializacao do Workload ----------
from m5.objects import SEWorkload
system.workload = SEWorkload.init_compatible(args.cmd)

process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Simulacao iniciada...")
exit_event = m5.simulate()
print("Simulacao finalizada!")
