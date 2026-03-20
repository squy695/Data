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
    'adservice': 1, 'cartservice': 1, 'checkoutservice': 1,
    'currencyservice': 4, 'emailservice': 1, 'frontend': 3,
    'paymentservice': 1, 'productcatalogservice': 1,
    'recommendationservice': 2, 'shippingservice': 1
}
columns = list(service_weights.keys())
reference_vector = np.array([service_weights[col] for col in columns])

# Define experiment methods and visual parameters
methods = ['Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
method_zorder = [20, 10, 0, 0, 0, 0, 0]
group_base_colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']

# Data file paths
csv_files_all = [[f'data/{m.replace(" (", " ").replace(")", "")}/{i}/count.csv' for i in range(1, 4)] for m in methods]
csv_files_plot = [[group[0]] for group in csv_files_all]

# Pre-calculate average distance metrics
distances_map = {method: 0 for method in methods}
for idx, group in enumerate(csv_files_all):
    valid_files = 0
    for file in group:
        if os.path.isfile(file):
            df = pd.read_csv(file, sep=None, engine='python')[columns]
            # Calculate L1 distance to reference vector
            distances_map[methods[idx]] += np.mean(df.apply(lambda r: np.sum(np.abs(r.values - reference_vector)), axis=1))
            valid_files += 1
    if valid_files > 0:
        distances_map[methods[idx]] /= valid_files

# Initialize plot
fig, ax = plt.subplots(figsize=(14, 7))

# Plot primary curves
for idx, group in enumerate(csv_files_plot):
    base_color = group_base_colors[idx]
    file = group[0]
    
    if os.path.isfile(file):
        df = pd.read_csv(file, sep=None, engine='python')[columns]
        distances = df.apply(lambda r: np.sum(np.abs(r.values - reference_vector)), axis=1).tolist()
        x = np.linspace(0, 15, len(distances))
        
        ax.plot(
            x, distances,
            label=methods[idx],
            color=base_color,
            linewidth=2,
            marker=markers[idx],
            markersize=7 if markers[idx] in ['*', 'x'] else 5,
            markeredgewidth=2 if markers[idx] in ['*', 'x'] else 1,
            zorder=method_zorder[idx],
            markevery=1 # Adjust if markers are too dense
        )

# Legend configuration
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5
)

# Highlight over-allocation points
for x, y in zip([0, 0.53571429], [12, 9]):
    ax.plot(x, y, marker='o', label='Over-allocation', markersize=10, 
            markeredgewidth=2, markeredgecolor=group_base_colors[1], 
            markerfacecolor='none', linestyle='none')

# Axis and grid styling
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Distance to Optimal Allocation', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Save and export
plt.tight_layout()
plt.savefig("fig_11_b.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()