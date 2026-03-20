import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib import rcParams

# Plotting style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

fig, ax = plt.subplots(figsize=(15, 8.5))
ax2 = ax.twinx()

# Color and marker configuration for different metrics
group_base_colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1']
markers = ['D', 's', 'o', '^', '*', 'x']
interfaces = ['/homepage', '/product1', '/product2', '/cart', '/pay']
services = ['cartservice', 'checkoutservice', 'currencyservice', 'frontend', 'productcatalogservice', 'recommendationservice']
simple_service = {s: s.replace('service', '') for s in services}

# Process and plot Actual Workload (Left Axis)
ccu_files = ['homepage', 'product1', 'product2', 'cart', 'pay']
for i, filename in enumerate(ccu_files):
    file_path = f"actual workload/{filename}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Normalize workload values
        uc = df['workload'] / 20
        x = np.linspace(0, 60, len(uc))
        ax.plot(x, uc, alpha=0.2, label=interfaces[i], color=group_base_colors[i])

# Configure Left Axis
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Actual workload (AOL = 1s)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.set_ylim(20, 115)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Process and plot CPU Usage (Right Axis)
q_file = "quantified workload/cpu usage total.csv"
if os.path.exists(q_file):
    df_q = pd.read_csv(q_file).fillna(0)
    for index, service in enumerate(services):
        if service in df_q.columns:
            uc_q = df_q[service].to_numpy()
            x_q = np.linspace(0, 60, len(uc_q))
            
            # Dynamic marker sizing
            is_special = markers[index] in ['*', 'x']
            msize = 7 if is_special else 5
            mwidth = 2 if is_special else 1
            
            ax2.plot(x_q, uc_q, label=simple_service[service], color=group_base_colors[index], 
                     linewidth=1.5, marker=markers[index], markevery=15,
                     markersize=msize, markeredgewidth=mwidth)

# Configure Right Axis
ax2.set_ylabel('Total CPU usage (millicore)', fontsize=32, fontweight='bold')
ax2.tick_params(axis='y', labelsize=28)
ax2.set_ylim(-30, 580)

# Multi-legend handling
leg1 = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.89), ncol=5, frameon=False, 
                fontsize=28, handletextpad=0, columnspacing=1.3, borderpad=0.5)
ax.add_artist(leg1)

leg2 = ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, frameon=False, 
                 fontsize=28, handletextpad=0, columnspacing=1.3, borderpad=0.5)

# Save high-resolution PDF output
plt.tight_layout()
plt.savefig("fig_CPU_usage_vs_workload.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()