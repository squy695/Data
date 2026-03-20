import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import rcParams
import pandas as pd
from math import nan
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D

# Global style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')

counts = [1, 2, 4, 8, 16, 32, 64]
markers = ['v', 'o', 's', '^', 'D', 'P', '*']
base = 0.4

# Collect all Z values for global normalization
all_z_values = []
for count in counts:
    df_avg = pd.read_csv(f'instance count={count}/avg latency HTTP code 200.csv')
    z_avg = np.power(df_avg['avg'], base)
    all_z_values.extend(z_avg)

# Logarithmic normalization based on power-transformed range
global_norm = LogNorm(vmin=np.min(all_z_values), vmax=np.max(all_z_values))

# Plotting data points
for index, count in enumerate(counts):
    # Load metrics
    df_avg = pd.read_csv(f'instance count={count}/avg latency HTTP code 200.csv')
    df_fail = pd.read_csv(f'instance count={count}/avg latency HTTP code 500.csv')
    df_workload = pd.read_csv(f'instance count={count}/workload.csv')

    # Data transformation and alignment
    x_avg = np.power(df_workload['workload'], base)
    x_avg = x_avg[::3][:579]
    z_avg = np.power(df_avg['avg'], base)
    x_fail = x_avg.copy()
    z_fail = np.power(df_fail['avg'], base)

    # Log-scale mapping for Y-axis (Instances)
    y_avg = np.full_like(x_avg, count)
    y_avg = np.log(y_avg) / np.log(2)
    y_fail = y_avg.copy()

    # Scatter plots for successful and failed requests
    sc = ax.scatter(x_avg, y_avg, z_avg, c=z_avg, cmap='Spectral_r', 
                    marker='o', norm=global_norm)
    sc = ax.scatter(x_fail, y_fail, z_fail, c=z_fail, cmap='Spectral_r',
                    marker='D', norm=global_norm)

# Colorbar configuration
cbar = fig.colorbar(sc, ax=ax, pad=0.01, location='right', aspect=20, shrink=0.5)

def inverse_transform(z_transformed):
    """Restore original units from power transformation"""
    return z_transformed ** (1/base)

# Map ticks in transformed space to original values for readability
ticks = np.linspace(np.min(all_z_values), np.max(all_z_values), 6)
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{inverse_transform(t):.0f}" for t in ticks])
cbar.minorticks_off()

# Axis labeling
ax.set_xlabel('Workload', fontsize=16, labelpad=10)
ax.set_ylabel('# of Instances', fontsize=16, labelpad=10)
ax.set_zlabel('Latency (ms)', fontsize=16, labelpad=13)

# X-axis tick mapping
xticklabels = [int(np.power(i, 1 / base)) for i in range(0, 16, 2)]
ax.set_xticks(range(0, 16, 2))
ax.set_xticklabels([str(c) for c in xticklabels])

# Y-axis tick mapping (Linear spacing for log-transformed values)
y_positions = np.arange(len(counts)+1)
ax.set_yticks(y_positions)
ax.set_yticklabels([str(c) for c in counts] + [''])

# Z-axis tick mapping
zticklabels = [int(np.power(i, 1 / base)) for i in range(0, 61, 10)]
ax.set_zticks(range(0, 61, 10))
ax.set_zticklabels([str(c) for c in zticklabels])
ax.tick_params(axis='z', pad=10)

# Pane and grid styling
ax.xaxis.pane.set_facecolor('white')
ax.yaxis.pane.set_facecolor('white')
ax.zaxis.pane.set_facecolor('white')

ax.grid(True)
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis._axinfo['grid']['linestyle'] = '--'
    axis._axinfo['grid']['linewidth'] = 0.5
    axis._axinfo['grid']['color'] = (0, 0, 0, 0.2)

# Camera angle
ax.view_init(elev=12, azim=215)

# Custom legend handles
custom_lines = [
    Line2D([0], [0], marker='o', color='w', label='HTTP status code 200',
           markerfacecolor='black', markersize=8),
    Line2D([0], [0], marker='D', color='w', label='HTTP status code 500',
           markerfacecolor='black', markersize=8)
]

# Position legend in the figure space
fig.legend(
    handles=custom_lines,
    loc='lower center',
    bbox_to_anchor=(0.58, 0.72),
    ncol=2,
    frameon=False,
    fontsize=18,
    handletextpad=0.02,
    labelspacing=0.05,
    columnspacing=0.5,
)

plt.tight_layout()
plt.savefig("fig 3a uncut.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.25)
plt.show()