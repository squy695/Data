import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os

# Scientific plotting style settings
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# File paths and corresponding labels
files = [
    'Squanler Good AOL/1/p90.csv',
    'Squanler Bad AOL/1/p90.csv',
    'Showar/1/p90.csv',
    'MicroScaler/1/p90.csv',
    'PBScaler/1/p90.csv',
    'Derm/1/p90.csv',
    'KHPA/1/p90.csv',
]

methods = [
    'Squanler (Good AOL)',
    'Squanler (Bad AOL)',
    'SHOWAR',
    'Microscaler',
    'PBScaler',
    'Derm',
    'KHPA'
]

group_base_colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
method_zorder = [20, 10, 0, 0, 0, 0, 0]
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
SLO = 500

fig, ax = plt.subplots(figsize=(14, 7))

# Iterate through files to read data and plot curves
for index, filepath in enumerate(files):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        continue
    try:
        data = pd.read_csv(filepath)
        if 'avg' in data.columns:
            y_values = data['avg']
            x = np.linspace(0, 15, len(y_values))
            
            # Use specific marker settings for visibility
            is_special_marker = markers[index] in ['*', 'x']
            ax.plot(
                x, y_values, 
                label=methods[index], 
                color=group_base_colors[index],
                linewidth=2, 
                marker=markers[index], 
                markersize=7 if is_special_marker else 5, 
                markeredgewidth=2 if is_special_marker else 1,
                markevery=8, 
                zorder=method_zorder[index]
            )
        else:
            print(f"Column 'avg' not found in {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

# Axis labels and tick configuration
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Avg P90 Latency (ms)', fontsize=32, fontweight='bold')
ax.tick_params(axis='x', labelsize=28)
ax.tick_params(axis='y', labelsize=28)

# Grid and horizontal SLO indicator line
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.axhline(y=SLO, color='gray', linestyle='--', linewidth=2)
ax.text(x=ax.get_xlim()[0] - 0.1, y=SLO, s='SLO', 
        ha='right', va='center', fontsize=20, fontweight='bold', color='gray')

# Vertical range adjustment for legend space
ax.set_ylim(ax.get_ylim()[0] - 600, ax.get_ylim()[1] * 1.28)

# Top-aligned horizontal legend
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    bbox_transform=ax.transAxes,
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5,
)

# Annotate specific event intervals
intervals = [(6, 10, 'server crash')]
for start, end, label in intervals:
    center = (start + end) / 2
    ax.axvspan(start, end, alpha=0.2, color='lightgray')
    ax.text(center, ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.07, 
            label, ha='center', va='top', fontsize=20)

# Final layout and export as PDF
plt.tight_layout()
plt.savefig("fig_12_b.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()