import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Scientific style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Load datasets and handle missing values
df_normal = pd.read_csv('latency HTTP code 200.csv').replace(0, np.nan)
df_fail = pd.read_csv('latency HTTP code 500.csv').replace(0, np.nan)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.linspace(0, 30, len(df_normal.index))

# Plot latency for HTTP 200 and 500 cases
target_col = '/ && GET'
if target_col in df_normal.columns:
    ax.plot(x, df_normal[target_col], color='#b0b35a', marker='D', markersize=5, 
            markevery=10, linestyle='-', linewidth=1.5, label='HTTP status code 200')

if target_col in df_fail.columns:
    ax.plot(x, df_fail[target_col], color='#f39851', marker='s', markersize=5, 
            markevery=10, linestyle='-', linewidth=1.5, label='HTTP status code 500')

# Axis labeling and tick configuration
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Latency (ms)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Legend placement above the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=2, 
          fontsize=28, frameon=False, handletextpad=0.5, columnspacing=1.3)

# Adjust Y-axis limits for annotation space
y_min, y_max = ax.get_ylim()
ax.set_ylim(y_min - 700, y_max * 1.1)

# Experimental phases and noise injection definitions
intervals = [
    (0, 5, 'No Noise'),
    (5, 10, 'Pod Failure'),
    (10, 15, 'Server Crash'),
    (15, 20, 'Background\nBatch Jobs'),
    (20, 25, 'Frequent\nAutoscaling'),
    (25, 30, 'Interference\nFrom Other APIs')
]

# Apply background shading and phase text labels
for i, (start, end, label) in enumerate(intervals):
    facecolor = 'lightgray' if i % 2 != 0 else 'white'
    ax.axvspan(start, end, alpha=0.2 if facecolor == 'lightgray' else 1.0, color=facecolor)
    
    # Position text labels at the bottom of each phase column
    ax.text((start + end) / 2, ax.get_ylim()[0] + (y_max - y_min) * 0.1, 
            label, ha='center', va='top', fontsize=20)

plt.tight_layout()
plt.savefig('fig_5_a.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()