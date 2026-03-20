import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.interpolate import make_interp_spline
import os

# Style Settings
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Configuration
columns = ['/ GET']
methods = ['200', '400', '600']
csv_groups = [
    ['SLO=200/1/avg.csv', 'SLO=200/2/avg.csv', 'SLO=200/3/avg.csv'], 
    ['SLO=400/1/avg.csv', 'SLO=400/2/avg.csv', 'SLO=400/3/avg.csv'],
    ['SLO=600/1/avg.csv', 'SLO=600/2/avg.csv', 'SLO=600/3/avg.csv'],    
]

group_colors = ['#14907e', '#e65050', '#7b5bb1']
markers = ['D', 's', 'o', '^', '*', 'x']

fig, ax = plt.subplots(figsize=(14, 7))

# Data Processing and Plotting
for group_idx, files in enumerate(csv_groups):
    group_data = []
    base_color = group_colors[group_idx % len(group_colors)]

    for file in files:
        if os.path.exists(file):
            try:
                # Load data, skip warm-up rows (1-10), and take the first 120 points
                df = pd.read_csv(file, sep=None, engine='python', skiprows=range(1, 11))
                group_data.append(df[columns].head(120).values.flatten())
            except Exception as e:
                print(f"Error reading {file}: {e}")

    if not group_data:
        continue

    # Calculate statistics across trials
    data_array = np.array(group_data)
    mean_dist = np.mean(data_array, axis=0)
    min_dist = np.min(data_array, axis=0)
    max_dist = np.max(data_array, axis=0)
    
    # Generate X-axis (0 to 15 minutes)
    x = np.linspace(0, 15, len(mean_dist))
    x_smooth = np.linspace(x.min(), x.max(), 300)

    # Spline Interpolation for Smooth Curves
    def smooth(y):
        return make_interp_spline(x, y, k=2)(x_smooth)

    y_mean = smooth(mean_dist)
    y_min = smooth(min_dist)
    y_max = smooth(max_dist)

    # Plot Mean Latency
    ax.plot(x_smooth, y_mean,
            marker=markers[group_idx],
            markersize=7 if markers[group_idx] in ['*', 'x'] else 5,
            markevery=15, # Adjusted for better visibility on smooth curves
            label=f'SLO={methods[group_idx]}ms', 
            color=base_color, 
            linewidth=2)

    # Plot Shaded Variance Area (Min-Max)
    ax.fill_between(x_smooth, y_min, y_max, color=base_color, alpha=0.2)

# Axis and Legend Formatting
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Avg Latency (ms)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Horizontal SLO Reference Lines
for val in [200, 400, 600]:
    ax.axhline(y=val, color='gray', linestyle='--', linewidth=2, alpha=0.6)

ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 0.988),
    ncol=3,
    frameon=False,
    fontsize=28,
    columnspacing=1.2
)

plt.tight_layout()
plt.savefig("fig_10.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()