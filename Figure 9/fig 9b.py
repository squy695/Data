import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os

# Academic style settings
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Configuration for paths, labels, and styles
files = [
    'data/Squanler Good AOL/1/p90.csv',
    'data/Squanler Bad AOL/1/p90.csv',
    'data/Showar/1/p90.csv',
    'data/Microscaler/1/p90.csv',
    'data/PBScaler/1/p90.csv',
    'data/Derm/1/p90.csv',
    'data/KHPA/1/p90.csv',
]

methods = ['Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
zorders = [20, 10, 0, 0, 0, 0, 0]
SLO = 500

fig, ax = plt.subplots(figsize=(14, 7))

# Single loop for data processing and plotting
for i, (path, method) in enumerate(zip(files, methods)):
    if not os.path.exists(path):
        continue
        
    try:
        df = pd.read_csv(path)
        if 'avg' not in df.columns:
            continue
            
        latency = df['avg']
        x_axis = np.linspace(0, 60, len(latency))

        # Calculate and print violation ratio for reference
        violation_ratio = (latency > SLO).sum() / len(latency)
        print(f"{method} Violation: {violation_ratio:.2%}")

        # Plot performance curves
        ax.plot(
            x_axis, latency, 
            label=method, 
            color=colors[i],
            linewidth=2, 
            marker=markers[i], 
            markersize=7 if markers[i] in ['*', 'x'] else 5, 
            markevery=30, 
            markeredgewidth=2 if markers[i] in ['*', 'x'] else 1,
            zorder=zorders[i]
        )
    except Exception as e:
        print(f"Error reading {path}: {e}")

# Axes and labels formatting
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Average P90 Latency (ms)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Threshold line for SLO
ax.axhline(y=SLO, color='gray', linestyle='--', linewidth=2)
ax.text(x=ax.get_xlim()[0] - 0.35, y=SLO, s='SLO', 
        ha='right', va='center', fontsize=20, fontweight='bold', color='gray')

# Top-centered legend configuration
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5
)

# Export high-resolution PDF
plt.tight_layout()
plt.savefig("fig_9_b.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()