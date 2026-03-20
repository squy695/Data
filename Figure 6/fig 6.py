import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib import rcParams
import matplotlib.colors as mcolors

# Scientific plotting style
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

methods = ['Squanler', 'SHOWAR', 'Microscaler', 'PBScaler', 'Derm', 'KHPA']
ccu_cases = ['without Condition 2 + 1×workload', 'with Condition 2 + 1×workload']

colors = ['#b0b35a', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']

fig, ax = plt.subplots(figsize=(14, 7))

# Layout constants
BOX_WIDTH = 0.15
GROUP_SPACING = 1.0
JITTER_WIDTH = 0.05

group_centers = []
legend_handles = []

for method_idx, method in enumerate(methods):
    group_center = method_idx * GROUP_SPACING
    group_centers.append(group_center)
    
    # Calculate normalization base per method (max value across all its cases)
    all_method_values = []
    for ccu_case in ccu_cases:
        file_path = f"{method}/{ccu_case}.csv"
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                # Sample 34 points evenly
                df = df.iloc[::max(1, len(df)//34), :]
                row_sums = df.sum(axis=1)
                all_method_values.extend(row_sums.values)
            except Exception:
                continue
    
    norm_base = np.max(all_method_values) if all_method_values else 1.0

    # Plot each case for the current method
    for ccu_idx, ccu_case in enumerate(ccu_cases):
        file_path = f"{method}/{ccu_case}.csv"
        if not os.path.exists(file_path):
            continue
            
        try:
            df = pd.read_csv(file_path)
            df = df.iloc[::max(1, len(df)//34), :]
            norm_y = df.sum(axis=1) / norm_base
            
            # Position boxes symmetrically around group center
            x_pos = group_center - 0.1 + (ccu_idx * 0.2)
            
            # Draw boxplot
            is_filled = (ccu_idx == 1)
            bp = ax.boxplot(
                norm_y, 
                positions=[x_pos],
                widths=BOX_WIDTH,
                patch_artist=True,
                boxprops=dict(
                    facecolor=mcolors.to_rgba(colors[method_idx], alpha=0.5) if is_filled else 'none',
                    edgecolor=colors[method_idx], 
                    linewidth=1.5
                ),
                medianprops=dict(color=colors[method_idx], linewidth=1.5),
                whiskerprops=dict(color=colors[method_idx], linestyle='--', linewidth=1.5),
                capprops=dict(color=colors[method_idx], linewidth=1.5),
                showfliers=False
            )

            # Extract handles for legend using the first method's boxes
            if method_idx == 0:
                legend_handles.append(bp["boxes"][0])

            # Overlay jittered scatter points
            jitter = np.random.uniform(-JITTER_WIDTH, JITTER_WIDTH, len(norm_y))
            ax.scatter(
                x_pos + jitter,
                norm_y,
                c=colors[method_idx],
                marker='o',
                alpha=0.5,
                s=28
            )
            
        except Exception as e:
            print(f"Error processing {method}/{ccu_case}: {e}")

# Axis and label configuration
ax.set_xticks(group_centers)
ax.set_xticklabels(methods, fontsize=12)

# Add group separators
for i in range(len(methods) - 1):
    ax.axvline((i + 0.5) * GROUP_SPACING, color='gray', linestyle=':', alpha=0.5)

ax.set_ylabel('Total # of instances (normalized)', fontsize=32, fontweight='bold')
ax.tick_params(axis='x', labelsize=24)
ax.tick_params(axis='y', labelsize=28)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7, axis='y')

# Legend setup
if legend_handles:
    ax.legend(
        legend_handles, 
        ccu_cases,
        loc='lower right', 
        fontsize=24,
        frameon=True,
        bbox_to_anchor=(0.88, 0.0),
        fancybox=True
    )

plt.tight_layout()
plt.savefig("fig_6.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()