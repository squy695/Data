import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import os

# Scientific plotting style configuration
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# List of service columns to be aggregated
service_columns = [
    'frontend', 'adservice', 'cartservice', 'checkoutservice', 
    'currencyservice', 'emailservice', 'paymentservice', 
    'productcatalogservice', 'recommendationservice', 'shippingservice'
]

# File paths and corresponding labels
files = [
    'Squanler Good AOL/1/count.csv',
    'Squanler Bad AOL/1/count.csv',
    'Showar/1/count.csv',
    'MicroScaler/1/count.csv',
    'PBScaler/1/count.csv',
    'Derm/1/count.csv',
    'KHPA/1/count.csv',
]

methods = [
    'Squanler (Good AOL)',
    'Squanler (Bad AOL)',
    'SHOWAR',
    'Microscaler',
    'PBScaler',
    'Derm',
    'KHPA'
]

group_base_colors = ['#b0b35a', '#14907e', '#f39851', '#e65050', '#3572ef', '#7b5bb1', '#adac9a']
markers = ['D', 's', 'o', '^', '*', 'x', 'v']
method_zorder = [20, 10, 0, 0, 0, 0, 0]

# Specific data indices to highlight with hollow markers
mark_points = {
    'Squanler (Good AOL)': 16,
    'Squanler (Bad AOL)': 16,
    'Microscaler': 20,
    'SHOWAR': 20,
    'PBScaler': 20,
    'Derm': 21,
    'KHPA': 21,
}

main_handles = []
main_labels = []

fig, ax = plt.subplots(figsize=(14, 7))

# Process and plot instance count for each method
for index, filepath in enumerate(files):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        continue
        
    try:
        data = pd.read_csv(filepath)
        available_cols = [col for col in service_columns if col in data.columns]

        if not available_cols:
            continue

        # Aggregate instance counts and generate time axis
        summed = data[available_cols].sum(axis=1)
        x = np.linspace(0, 15, len(summed))

        # Plot primary trend lines
        line, = ax.plot(
            x, summed, 
            label=methods[index], 
            color=group_base_colors[index],
            linewidth=2, 
            marker=markers[index], 
            markersize=7 if markers[index] in ['*', 'x'] else 5, 
            markeredgewidth=2 if markers[index] in ['*', 'x'] else 1,
            markevery=1, 
            zorder=method_zorder[index]
        )
        main_handles.append(line)
        main_labels.append(methods[index])

        # Add hollow circle markers at designated detection points
        method_name = methods[index]
        if method_name in mark_points:
            pt_idx = mark_points[method_name]
            if pt_idx < len(summed):
                ax.plot(
                    x[pt_idx], summed[pt_idx], 
                    marker='o', 
                    markersize=12, 
                    markeredgewidth=2, 
                    markeredgecolor=group_base_colors[index], 
                    markerfacecolor='none', 
                    linestyle='none'
                )

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Legend configuration
ax.legend(
    main_handles,
    main_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.05),
    ncol=3,
    frameon=False,
    fontsize=26,
    handletextpad=0.2,
    columnspacing=1.5
)

# Axis labels and tick formatting
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Total # of Instances', fontsize=32, fontweight='bold')
ax.tick_params(axis='x', labelsize=28)
ax.tick_params(axis='y', labelsize=28)
ax.set_ylim(ax.get_ylim()[0] - 6, ax.get_ylim()[1] * 1.28)

# Interval annotations for events
intervals = [(6, 10, 'server crash')]
for start, end, label in intervals:
    center = (start + end) / 2
    # Background span for the interval
    ax.axvspan(start, end, alpha=0.2, color='lightgray')
    # Text annotation for the event
    ax.text(
        center, 
        ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.07, 
        label, 
        ha='center', va='top', 
        fontsize=20
    )

ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Export as high-resolution PDF
plt.tight_layout()
plt.savefig("fig_12_a.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()