import os
import re
import matplotlib.pyplot as plt

# Diretório base dos resultados
results_dir = "./results"
cores_list = [1, 2, 4]
latencies_list = [30, 50, 100]

data = {}

# Extração dos dados
for c in cores_list:
    for l in latencies_list:
        filepath = os.path.join(results_dir, f"{c}_cores_{l}ns", "stats.txt")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
                
                # Buscando as métricas desejadas no stats.txt
                sim_match = re.search(r'simSeconds\s+([\d\.]+)', content)
                l2_match = re.search(r'board\.cache_hierarchy\.l2-cache-0\.overallMissRate::total\s+([\d\.]+)', content)
                
                sim_seconds = float(sim_match.group(1)) if sim_match else 0.0
                l2_miss = float(l2_match.group(1)) if l2_match else 0.0
                
                data[(c, l)] = {'simSeconds': sim_seconds, 'l2MissRate': l2_miss}
        else:
            print(f"Aviso: Arquivo não encontrado - {filepath}")

# Estilos dos gráficos
colors = {1: '#1f77b4', 2: '#ff7f0e', 4: '#2ca02c'}
markers = {1: 'o', 2: 's', 4: '^'}
linestyles = {1: '-', 2: '--', 4: ':'}

os.makedirs(os.path.join(results_dir, "graficos"), exist_ok=True)

# -------------------------------------------------------------
# Gráfico 1: Tempo de Execução vs Latência
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
for c in cores_list:
    x = latencies_list
    y = [data.get((c, l), {}).get('simSeconds', 0) for l in latencies_list]
    plt.plot(x, y, label=f'{c} Núcleo(s)', color=colors[c], marker=markers[c], 
             linewidth=2.5, markersize=8, linestyle=linestyles[c])

plt.title('Tempo de Execução vs Latência da Memória', fontsize=16, fontweight='bold')
plt.xlabel('Latência da Memória (ns)', fontsize=14)
plt.ylabel('Tempo de Execução (simSeconds)', fontsize=14)
plt.xticks(latencies_list, [f"{l}ns" for l in latencies_list], fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Configuração", fontsize=12, title_fontsize=13)
plt.tight_layout()

out_file1 = os.path.join(results_dir, "graficos", 'grafico_tempo_execucao.png')
plt.savefig(out_file1, dpi=300)
print(f"Gráfico 1 salvo em: {out_file1}")

# -------------------------------------------------------------
# Gráfico 2: Taxa de Cache Miss (L2) vs Latência
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
for c in cores_list:
    x = latencies_list
    y = [data.get((c, l), {}).get('l2MissRate', 0) for l in latencies_list]
    plt.plot(x, y, label=f'{c} Núcleo(s)', color=colors[c], marker=markers[c], 
             linewidth=2.5, markersize=8, linestyle=linestyles[c])

plt.title('Taxa de Faltas na Cache L2 vs Latência da Memória', fontsize=16, fontweight='bold')
plt.xlabel('Latência da Memória (ns)', fontsize=14)
plt.ylabel('Cache Miss Rate (Taxa)', fontsize=14)
plt.xticks(latencies_list, [f"{l}ns" for l in latencies_list], fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Configuração", fontsize=12, title_fontsize=13)
plt.tight_layout()

out_file2 = os.path.join(results_dir, "graficos", 'grafico_l2_miss_rate.png')
plt.savefig(out_file2, dpi=300)
print(f"Gráfico 2 salvo em: {out_file2}")

print("Todos os gráficos foram gerados e salvos com sucesso na pasta results/graficos!")
