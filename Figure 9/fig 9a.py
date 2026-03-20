import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os

# Academic style settings
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Configuration
service_columns = [
    'adservice', 'cartservice', 'checkoutservice', 'currencyservice',
    'emailservice', 'frontend', 'paymentservice', 'productcatalogservice',
    'recommendationservice', 'redis-cart', 'shippingservice'
]

pod_max_values = {'Microscaler': 13, 'default': 14}

files = [
    'data/Squanler Good AOL/1/count.csv',
    'data/Squanler Bad AOL/1/count.csv',
    'data/Showar/1/count.csv',
    'data/Microscaler/1/count.csv',
    'data/PBScaler/1/count.csv',
    'data/Derm/1/count.csv',
    'data/KHPA/1/count.csv',
]

methods = ['Squanler (Good AOL)', 'Squanler (Bad AOL)', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
zorders = [20, 10, 0, 0, 0, 0, 0]

fig, ax = plt.subplots(figsize=(14, 7))
main_handles = []

# Process and plot each method
for i, (path, method) in enumerate(zip(files, methods)):
    if not os.path.exists(path):
        continue
        
    try:
        data = pd.read_csv(path)
        # Filter existing columns and calculate total instances
        cols = [c for c in service_columns if c in data.columns]
        summed = data[cols].sum(axis=1)
        x = np.linspace(0, 60, len(summed))

        line, = ax.plot(
            x, summed, 
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

        # Highlight over-allocation for specific method
        if method == 'Squanler (Bad AOL)':
            pt_idx = 1 # Specific index to highlight
            ax.plot(x[pt_idx], summed.iloc[pt_idx], 
                    marker='o', markersize=12, markeredgewidth=2,
                    markeredgecolor=colors[i], markerfacecolor='none',
                    linestyle='none', zorder=25)

    except Exception as e:
        print(f"Error processing {method}: {e}")

# Axes formatting
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Total # of Instances', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.28)

# Top legend configuration
if main_handles:
    ax.legend(
        handles=main_handles,
        labels=methods,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        frameon=False,
        fontsize=26,
        handletextpad=0.2,
        columnspacing=1.5
    )

plt.tight_layout()
plt.savefig("fig_9_a.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()