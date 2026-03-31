import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib import rcParams

# Set academic plotting style
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

# Define labels for workload interfaces
interfaces = [
    '/ && GET', '/login && GET', '/customers && GET', 
    '/category.html && GET', '/detail.html?id={} && GET', 
    '/cart && DELETE', '/cart && POST', '/basket.html && GET'
]

fig, ax = plt.subplots(figsize=(14, 8))

# Process workload files wiki 1.csv to wiki 8.csv
for i in range(1, 9):
    file_path = os.path.join("workload/wiki/", f"wiki {i}.csv")
    
    if os.path.exists(file_path):
        # Read and normalize workload data
        df = pd.read_csv(file_path)
        y = df['count'] * 0.7 / 20
        x = np.linspace(0, 60, len(y))

        # Plot workload curve for each interface
        ax.plot(x, y, label=interfaces[i-1])

# Configure axis labels and ticks
ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Workload', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)

# Configure top-center legend with horizontal layout
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 0.988),
    ncol=4,
    frameon=False,
    fontsize=12
)

# Export as high-resolution PDF
plt.tight_layout()
plt.savefig("workload.pdf", format='pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()