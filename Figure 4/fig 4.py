import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import matplotlib.colors as mcolors

# Global scientific style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

methods = ['Squanler', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
colors = ['#b0b35a', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
ccu_cases = {'fall into Scenario 1 + 1×workload':1, 'fall into Scenario 1 + 2×workload':2}

# Plotting parameters
BOX_WIDTH, GROUP_SPACING, JITTER_WIDTH = 0.15, 1.0, 0.05
fig, ax = plt.subplots(figsize=(14, 7))

legend_handles = [None, None]

for m_idx, method in enumerate(methods):
    group_center = m_idx * GROUP_SPACING
    method_data = []
    
    # Load and process workload data for specific microservices
    for case in ccu_cases.keys():
        try:
            df = pd.read_csv(f"{method}/{ccu_cases[case]}.csv", nrows=50)
            services = ['frontend', 'currencyservice', 'productcatalogservice', 
                        'recommendationservice', 'cartservice', 'checkoutservice']
            method_data.append(df[services].sum(axis=1))
        except Exception as e:
            print(f"Skipping {method} {case}: {e}")
            method_data.append(None)
    
    # Normalize by the mean of the 1x workload baseline
    if all(d is not None for d in method_data):
        baseline_mean = np.mean(method_data[0])
        
        for i, y in enumerate(method_data):
            norm_y = y / baseline_mean
            x_pos = group_center - 0.1 + i * 0.2
            
            # Configure boxplot appearance
            is_filled = (i == 1)
            bp = ax.boxplot(
                norm_y, positions=[x_pos], widths=BOX_WIDTH, patch_artist=True,
                showfliers=False,
                boxprops=dict(facecolor=mcolors.to_rgba(colors[m_idx], alpha=0.5 if is_filled else 0),
                              edgecolor=colors[m_idx], linewidth=1.5),
                medianprops=dict(color=colors[m_idx], linewidth=1.5),
                whiskerprops=dict(color=colors[m_idx], linestyle='--', linewidth=1.5),
                capprops=dict(color=colors[m_idx], linewidth=1.5)
            )
            
            # Extract legend handles from the first method iteration
            if m_idx == 0:
                legend_handles[i] = bp["boxes"][0]

            # Overlay jittered scatter points for data distribution
            ax.scatter(
                x_pos + np.random.uniform(-JITTER_WIDTH, JITTER_WIDTH, len(norm_y)),
                norm_y, c=colors[m_idx], marker='o', alpha=0.5, s=28
            )

# X-axis labeling
ax.set_xticks(np.arange(len(methods)) * GROUP_SPACING)
ax.set_xticklabels(methods, fontsize=24)

# Vertical separators between method groups
for i in range(len(methods) - 1):
    ax.axvline((i + 0.5) * GROUP_SPACING, color='gray', linestyle=':', alpha=0.5)

# Horizontal reference lines for theoretical targets
for h in [1, 2]:
    ax.axhline(y=h, color='gray', linestyle='--', linewidth=2, alpha=0.7)

# Labels and grid formatting
ax.set_ylabel('Total # of instances (normalized)', fontsize=32, fontweight='bold')
ax.tick_params(axis='y', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7, axis='y')

# Final legend construction
if all(legend_handles):
    ax.legend(legend_handles, ccu_cases.keys(), loc='upper right', fontsize=24, frameon=True)

plt.tight_layout()
plt.savefig("fig_4.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()