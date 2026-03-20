import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# Academic style settings
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Target service configuration and reference vector
service_weights = {
    'catalogue': 1, 
    'front-end': 6,
    'payment': 1, 
    'queue-master': 1, 
    'rabbitmq': 1, 
    'shipping': 1, 
    'user': 1
}
columns = list(service_weights.keys())
reference_vector = np.array([service_weights[col] for col in columns])

# Trial datasets for statistical calculation
csv_files_1 = [
    [f'data/Squanler Good AOL/{i}/count.csv' for i in range(1, 4)],
    [f'data/Squanler Bad AOL/{i}/count.csv' for i in range(1, 4)],
    [f'data/Showar/{i}/count.csv' for i in range(1, 4)],
    [f'data/MicroScaler/{i}/count.csv' for i in range(1, 4)],    
    [f'data/PBScaler/{i}/count.csv' for i in range(1, 4)],
    [f'data/Derm/{i}/count.csv' for i in range(1, 4)],
    [f'data/KHPA/{i}/count.csv' for i in range(1, 4)],
]

# Datasets for primary plotting
csv_files = [[g[0]] for g in csv_files_1]

methods = ['Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
method_zorder = [20, 10, 0, 0, 0, 0, 0]
group_base_colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']

# Calculate average distance metrics across all trials
total_map = {method: 0 for method in methods}
distances_map = {method: 0 for method in methods}

for group_idx, group in enumerate(csv_files_1):
    for file in group:
        if os.path.isfile(file):
            df = pd.read_csv(file, sep=None, engine='python')[columns]
            total_map[methods[group_idx]] += np.mean(df.sum(axis=1))
            # L1 Distance calculation
            distances_map[methods[group_idx]] += np.mean(df.apply(lambda row: np.sum(np.abs(row.values - reference_vector)), axis=1))

for method in distances_map:
    distances_map[method] /= 3

fig, ax = plt.subplots(figsize=(14, 7))

# Plot performance curves
for group_idx, group in enumerate(csv_files):
    base_color = group_base_colors[group_idx]
    for file_idx, file in enumerate(group):
        if not os.path.isfile(file): continue
        
        df = pd.read_csv(file, sep=None, engine='python')[columns]
        distances = df.apply(lambda row: np.sum(np.abs(row.values - reference_vector)), axis=1).tolist()
        x = np.linspace(0, 15, len(distances))

        ax.plot(
            x, distances,
            label=methods[group_idx] if file_idx == 0 else None,
            color=base_color,
            alpha=1.0 if file_idx == 0 else 0.25,
            linewidth=2,
            marker=markers[group_idx],
            markersize=7 if markers[group_idx] in ['*', 'x'] else 5,
            markeredgewidth=2 if markers[group_idx] in ['*', 'x'] else 1,
            zorder=method_zorder[group_idx]
        )

# Main legend setup
legend1 = ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    bbox_transform=ax.transAxes,
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5,
)
ax.add_artist(legend1)

# Annotate specific overestimation points
for x, y in zip([0, 0.53571429], [7, 7]):
    ax.plot(x, y, 
            marker='o', 
            markersize=10, 
            markeredgewidth=2, 
            markeredgecolor=group_base_colors[1], 
            markerfacecolor='none', 
            linestyle='none')

# Axis and grid configuration
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.tick_params(axis='x', labelsize=28)
ax.set_ylabel('Distance to Optimal Allocation', fontsize=32, fontweight='bold')
ax.tick_params(axis='y', labelsize=28)
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout()
plt.savefig("fig_11_a.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()