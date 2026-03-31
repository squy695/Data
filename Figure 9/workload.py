import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib import rcParams

# Set academic style
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Define labels for workload interfaces
interfaces = [
    '/ && GET', 
    '/product/{id}',
    '/cart && GET',
    '/cart/checkout && POST',
    '/setCurrency && POST'
]

fig, ax = plt.subplots(figsize=(14, 8))

# Process workload files wiki 1.csv to wiki 5.csv
for i in range(1, 6):
    file_path = f"workload/wiki {i}.csv"
    
    if os.path.exists(file_path):
        # Load count data and generate a 60-minute time axis
        df = pd.read_csv(file_path)
        y = df['count']
        x = np.linspace(0, 60, len(y))

        # Plot workload curve with corresponding interface label
        ax.plot(x, y, label=interfaces[i-1])

# Configure axis labels and ticks
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Workload', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)

# Configure top-center legend with horizontal layout
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 0.988),
    ncol=5,
    frameon=False,
    fontsize=12
)

# Export as high-resolution PDF
plt.tight_layout()
plt.savefig("workload.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()