import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Scientific style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Load and prepare CPU usage data
df_normal = pd.read_csv('CPU usage.csv')
fig, ax = plt.subplots(figsize=(14, 8))
x = np.linspace(0, 30, len(df_normal.index))

# Plotting aesthetics for microservices
colors = ['#b0b35a', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
services = ['frontend', 'currencyservice', 'cartservice']

# Plot selected services with distinct markers
for i, service in enumerate(services):
    if service in df_normal.columns:
        ax.plot(x, df_normal[service], color=colors[i], marker=markers[i], 
                markersize=5, markevery=10, linestyle='-', linewidth=1.5, label=service)

# Axis and grid formatting
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('CPU usage (millicore)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Legend configuration
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, 
          fontsize=24, frameon=False, handletextpad=0.5, columnspacing=1.3)

# Expand Y-axis for bottom phase labels
y_min, y_max = ax.get_ylim()
ax.set_ylim(y_min - 60, y_max * 1.1)

# Experimental noise phase definitions
intervals = [
    (0, 5, 'No Noise'),
    (5, 10, 'Pod Failure'),
    (10, 15, 'Server Crash'),
    (15, 20, 'Background\nBatch Jobs'),
    (20, 25, 'Frequent\nAutoscaling'),
    (25, 30, 'Interference\nFrom Other APIs')
]

# Apply phase shading and bottom annotations
for i, (start, end, label) in enumerate(intervals):
    if i % 2 != 0:
        ax.axvspan(start, end, alpha=0.2, color='lightgray')
    
    # Calculate vertical position for text labels
    center_x = (start + end) / 2
    label_y = ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.1
    ax.text(center_x, label_y, label, ha='center', va='top', fontsize=20)

plt.tight_layout()
plt.savefig('fig_5_c.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()