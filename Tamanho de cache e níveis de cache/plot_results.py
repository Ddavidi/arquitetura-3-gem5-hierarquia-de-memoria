import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

results_dir = '/home/bernardo-eng/projeto_arquitetura/results'

# Setup plotting style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.titlesize': 16, 'axes.titlesize': 14})

# Metrics to extract
metrics = {
    'simSeconds': 'Tempo de Execução (s)',
    'system.cpu.ipc': 'IPC',
    'system.cpu.cpi': 'CPI',
    'simInsts': 'Instruções Base',
    'system.cpu.dcache.overallMissRate::total': 'Taxa de Falha L1D',
    'system.cpu.dcache.overallMisses::total': 'Misses Absoluto L1D',
}

data = []

# Parse directories
for d in os.listdir(results_dir):
    dir_path = os.path.join(results_dir, d)
    if os.path.isdir(dir_path) and d.startswith('l1_') and '_l3_' in d:
        parts = d.split('_')
        try:
            l1_size_str = parts[1]
            l1_size_int = int(l1_size_str.replace('kB', ''))
            l2_bool = parts[3] == 'True'
            l3_bool = parts[5] == 'True'
        except Exception:
            continue
            
        # Determine scenario title
        if not l2_bool and not l3_bool:
            scenario = "Apenas L1"
        elif l2_bool and not l3_bool:
            scenario = "L1 + L2"
        elif not l2_bool and l3_bool:
            scenario = "L1 + L3 (Sem L2)"
        else:
            scenario = "L1 + L2 + L3"
            
        stats_file = os.path.join(dir_path, 'stats.txt')
        if not os.path.exists(stats_file):
            continue
            
        row = {
            'Cenário': scenario,
            'L1D_Size_kB': l1_size_int,
            'DirName': d,
            'L2': l2_bool,
            'L3': l3_bool
        }
        
        # Init metrics with None
        for k in metrics.keys():
            row[k] = None
            
        with open(stats_file, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts: continue
                metric_name = parts[0]
                if metric_name in metrics:
                    row[metric_name] = float(parts[1])
                    
        # Calculate MPKI if both required metrics are present
        if row['system.cpu.dcache.overallMisses::total'] is not None and row['simInsts'] is not None:
            # MPKI = OverallMisses / (simInsts / 1000)
            row['MPKI'] = row['system.cpu.dcache.overallMisses::total'] / (row['simInsts'] / 1000.0)
        else:
            row['MPKI'] = None
            
        data.append(row)

df = pd.DataFrame(data)
df = df.sort_values(by=['Cenário', 'L1D_Size_kB'])

# Ensure results directory exists for figures
figs_dir = '/home/bernardo-eng/projeto_arquitetura/results_figs'
os.makedirs(figs_dir, exist_ok=True)

# Define plotting helper
def plot_metric(metric, title, ylabel, filename):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='L1D_Size_kB', y=metric, hue='Cenário', style='Cenário', markers=True, dashes=True, linewidth=2.5, markersize=8, alpha=0.8)
    plt.title(title, pad=15, fontweight='bold')
    plt.ylabel(ylabel, fontweight='bold')
    plt.xlabel('Tamanho da Cache L1D (kB)', fontweight='bold')
    plt.xticks([8, 16, 32, 64])
    plt.legend(title='Hierarquia de Cache')
    plt.tight_layout()
    plt.savefig(os.path.join(figs_dir, filename), dpi=300)
    plt.close()

# 1. IPC - Instruções por Ciclo (Maior é melhor)
plot_metric('system.cpu.ipc', 
           'Desempenho (IPC) vs Tamanho da Cache L1D', 
           'IPC (Instruções por Ciclo)', 
           'ipc_vs_l1d.png')

# 2. CPI - Ciclos por Instrução (Menor é melhor)
plot_metric('system.cpu.cpi', 
           'Desempenho (CPI) vs Tamanho da Cache L1D', 
           'CPI (Ciclos por Instrução)', 
           'cpi_vs_l1d.png')

# 3. Taxa de Falha L1D (Menor é melhor)
plot_metric('system.cpu.dcache.overallMissRate::total', 
           'Taxa de Falha da L1D vs Tamanho da Cache L1D', 
           'Taxa de Falha L1D', 
           'missrate_vs_l1d.png')

# 4. MPKI (Menor é melhor)
plot_metric('MPKI', 
           'MPKI (Misses per Kilo Instructions) vs Tamanho da Cache L1D', 
           'MPKI', 
           'mpki_vs_l1d.png')

# 5. Tempo de Execução (simSeconds)
plot_metric('simSeconds', 
           'Tempo de Execução vs Tamanho da Cache L1D', 
           'Tempo de Execução Simulado (s)', 
           'simseconds_vs_l1d.png')

print("Visualizações geradas com sucesso em:", figs_dir)
df.to_csv(os.path.join(figs_dir, 'dados_compilados.csv'), index=False)
print("Dados compilados salvos em:", os.path.join(figs_dir, 'dados_compilados.csv'))
