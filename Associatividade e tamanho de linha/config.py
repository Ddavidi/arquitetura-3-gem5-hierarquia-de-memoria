import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--assoc",        type=int, default=4)
parser.add_argument("--line_size",    type=int, default=64)
parser.add_argument("--repl",         type=str, default="LRU")
parser.add_argument("--write_policy", type=str, default="wb")
parser.add_argument("--cmd",          type=str, default="/gem5/hello")
args = parser.parse_args()

repl_policies = {
    "LRU":    LRURP,
    "Random": RandomRP,
    "FIFO":   FIFORP,
    "LFU":    LFURP,
}
if args.repl not in repl_policies:
    print("Erro: use LRU, Random, FIFO ou LFU")
    exit(1)

ReplacementPolicy = repl_policies[args.repl]

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode   = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.cache_line_size = args.line_size
system.workload = SEWorkload.init_compatible(args.cmd)

system.cpu = X86TimingSimpleCPU()

system.cpu.icache = Cache(
    size="32kB", assoc=4, tag_latency=2, data_latency=2,
    response_latency=2, mshrs=4, tgts_per_mshr=20,
    replacement_policy=LRURP()
)
system.cpu.dcache = Cache(
    size="64kB", assoc=args.assoc, tag_latency=2, data_latency=2,
    response_latency=2, mshrs=4, tgts_per_mshr=20,
    replacement_policy=ReplacementPolicy()
)

system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

system.l2cache = Cache(
    size="256kB", assoc=8, tag_latency=20, data_latency=20,
    response_latency=20, mshrs=20, tgts_per_mshr=12,
    replacement_policy=LRURP()
)
system.l2cache.cpu_side = system.l2bus.mem_side_ports

system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio           = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Iniciando simulacao...")
print("  assoc=%d line_size=%d repl=%s write_policy=%s" % (
    args.assoc, args.line_size, args.repl, args.write_policy))

exit_event = m5.simulate()
print("Simulacao finalizada: %s" % exit_event.getCause())
print("Ticks: %d" % m5.curTick())
