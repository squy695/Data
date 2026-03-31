import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os

# Style Settings
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Configuration
service_columns = ['catalogue', 'front-end', 'payment', 'shipping', 'user']
pod_max_values = {'Microscaler': 19, 'default': 30}

methods = [
    'Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR',
    'Microscaler', 'PBScaler', 'Derm', 'KHPA'
]

files = [
    'data/Squanler Good AOL/1/count.csv',
    'data/Squanler Bad AOL/3/count.csv',
    'data/Showar/1/count.csv',
    'data/MicroScaler/1/count.csv',
    'data/PBScaler/1/count.csv',
    'data/Derm/1/count.csv',
    'data/KHPA/2/count.csv'
]

colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
zorders = [20, 10, 0, 0, 0, 0, 0]

# Pre-calculate Average Distances
distances_map = {}
for method, path in zip(methods, files):
    if os.path.exists(path):
        df = pd.read_csv(path, sep=None, engine='python')
        # Sum only available target columns per row
        valid_cols = [c for c in service_columns if c in df.columns]
        distances_map[method] = df[valid_cols].sum(axis=1).mean()

# Calculate relative difference for specific case
if 'Squanler (Bad AOL)' in distances_map and 'Squanler (Good AOL)' in distances_map:
    diff = (distances_map['Squanler (Bad AOL)'] - distances_map['Squanler (Good AOL)']) / distances_map['Squanler (Good AOL)']
    print(f"Relative Difference: {diff:.2%}")

# Plotting
fig, ax = plt.subplots(figsize=(14, 7))
main_handles = []

for i, (path, method) in enumerate(zip(files, methods)):
    if not os.path.exists(path):
        continue
    
    data = pd.read_csv(path)
    valid_cols = [c for c in service_columns if c in data.columns]
    
    # Calculate Total Instances (Y-axis) and Time (X-axis)
    summed = data[valid_cols].sum(axis=1)
    x_axis = np.linspace(0, 60, len(summed))

    # Plot Method Lines
    line, = ax.plot(
        x_axis, summed, 
        label=method, 
        color=colors[i],
        linewidth=2, 
        marker=markers[i], 
        markersize=7 if markers[i] in ['*', 'x'] else 5, 
        markevery=5, 
        markeredgewidth=2 if markers[i] in ['*', 'x'] else 1,
        zorder=zorders[i]
    )
    main_handles.append(line)

    # Highlight Specific Over-allocation Events
    if method == 'Squanler (Bad AOL)':
        points_to_mark = [1, 2] # Indices for highlight
        for pt in points_to_mark:
            if pt < len(x_axis):
                # Hollow circle to indicate over-estimation
                special_mark, = ax.plot(
                    x_axis[pt], summed.iloc[pt], 
                    marker='o', markersize=12, markeredgewidth=2, 
                    markeredgecolor=colors[i], markerfacecolor='none', 
                    linestyle='none', zorder=25
                )
                special_handle = special_mark

# Formatting & Legends
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Total # of Instances', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Top Legend: Primary Methods
if main_handles:
    ax.legend(
        handles=main_handles,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        frameon=False,
        fontsize=24,
        handletextpad=0.2,
        columnspacing=1.5
    )

plt.tight_layout()
plt.savefig("fig_8_a.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()