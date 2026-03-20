import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.lines import Line2D

# Scientific plot styling
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

APIs = ['API 1', 'API 2', 'API 3', 'API 4', 'API 5']
colors = ['#b0b35a', '#f39851', '#e65050', '#3572ef', '#7b5bb1']

fig, ax = plt.subplots(figsize=(14, 8))

# Constants for positioning
JITTER_WIDTH = 0.075
BOX_WIDTH = 0.15
bias = 0.1

boxplot_data = []

for index, api in enumerate(APIs):
    # Load data and compute CCpR (CPU cost per request)
    tps_data = pd.read_csv(f"{api}/rps.csv")
    cpu_data = pd.read_csv(f"{api}/total cpu usage.csv")
    
    # Calculate Y values, handling division by zero
    y_new = np.where(tps_data['avg'] != 0, cpu_data['avg'] / tps_data['avg'], np.nan)
    clean_data = y_new[~np.isnan(y_new)]
    boxplot_data.append(clean_data)

    # Plot jittered scatter points
    jitter = np.random.uniform(-JITTER_WIDTH, JITTER_WIDTH, size=len(y_new))
    ax.scatter(index + bias + jitter, y_new, c=colors[index], alpha=0.2, s=28)

# Plot Boxplots and Average labels
for index, data in enumerate(boxplot_data):
    if len(data) == 0: continue
    
    # Draw boxplot
    ax.boxplot(data, positions=[index - bias], widths=BOX_WIDTH, patch_artist=True,
               showfliers=False,
               boxprops=dict(facecolor='none', color=colors[index], linewidth=1.5),
               medianprops=dict(color=colors[index], linewidth=1.5),
               whiskerprops=dict(color=colors[index], linestyle='--', linewidth=1.5),
               capprops=dict(color=colors[index], linewidth=1.5))
    
    # Annotate mean value above the group
    mean_val = np.mean(data)
    text_y = np.max(data) + 0.01 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.text(index, text_y, f'Avg = {mean_val:.2f}', ha='center', va='bottom', fontsize=28)

# Axis formatting
ax.set_xticks(range(len(APIs)))
ax.set_xticklabels(APIs, fontsize=28)
ax.set_ylabel('CPU cost per request (CCpR)', fontsize=32, fontweight='bold')
ax.tick_params(axis='y', labelsize=28)
ax.grid(True, linestyle='--', alpha=0.7, axis='y')

# Vertical separators
for i in range(len(APIs)):
    ax.axvline(i - 0.5, color='gray', linestyle=':', alpha=0.3)

# Expand Y-axis for legends
ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * 1.45)

# Legend Construction
legend_elements = [Line2D([0], [0], marker='o', color=c, linestyle='none', markersize=12) for c in colors]

# Top legend: Primary metrics
leg1 = ax.legend(legend_elements[:3], ['CCpR₁', 'CCpR₂', 'CCpR₃'],
                 loc='upper center', bbox_to_anchor=(0.5, 1.02),
                 ncol=3, frameon=False, fontsize=28, handletextpad=0.2)
ax.add_artist(leg1)

# Lower legend: Composite formulas
labels_comp = [
    'CCpR₄ = (7CCpR₁ + 2CCpR₂ + 1CCpR₃) / 10', 
    'CCpR₅ = (1CCpR₁ + 2CCpR₂ + 4CCpR₃) / 7'
]
ax.legend(legend_elements[3:], labels_comp,
          loc='upper center', bbox_to_anchor=(0.5, 0.94),
          ncol=1, frameon=False, fontsize=28, handletextpad=0.2)

plt.tight_layout()
plt.savefig("fig_3_c.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()