import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os
from matplotlib.ticker import FuncFormatter

# Style Settings
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Configuration
SLO = 500
files = [
    'data/Squanler Good AOL/1/p90.csv',
    'data/Squanler Bad AOL/3/p90.csv',
    'data/Showar/1/p90.csv',
    'data/MicroScaler/1/p90.csv',
    'data/PBScaler/1/p90.csv',
    'data/Derm/1/p90.csv',
    'data/KHPA/2/p90.csv'
]

methods = [
    'Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR',
    'Microscaler', 'PBScaler', 'Derm', 'KHPA'
]

colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
zorders = [20, 10, 0, 0, 0, 0, 0]

# Calculation & Plotting
fig, ax = plt.subplots(figsize=(14, 7))
violation_results = {}

for i, (path, method) in enumerate(zip(files, methods)):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
        
    try:
        data = pd.read_csv(path)
        if 'avg' not in data.columns:
            continue
            
        latency = data['avg']
        x_axis = np.linspace(0, 60, len(latency))

        # Calculate SLO Violation Ratio
        v_ratio = (latency > SLO).sum() / len(latency)
        violation_results[method] = v_ratio

        # Plot Latency Curves
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
        print(f"Error processing {method}: {e}")

# Formatting
# Y-axis scaling: divide by 10 as per your requirement
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/10:g}'))

ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Avg P90 Latency (ms) (x10)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)

# Vertical headroom for legend
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# SLO Threshold Line
ax.axhline(y=SLO, color='gray', linestyle='--', linewidth=2)
ax.text(x=ax.get_xlim()[0] - 0.35, y=SLO + 800, s='SLO', 
        ha='right', va='center', fontsize=20, fontweight='bold', color='gray')

# Legend: Top-center, horizontal layout
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5
)

# Output
plt.tight_layout()
plt.savefig("fig_8_b.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()

# Print violation stats for verification
for m, r in violation_results.items():
    print(f"{m} Violation Rate: {r:.2%}")