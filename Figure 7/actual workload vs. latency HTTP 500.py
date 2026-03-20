import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import spearmanr

# Scientific plotting style
rcParams['font.family'] = 'Times New Roman'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.linewidth'] = 1.2

fig, ax = plt.subplots(figsize=(15, 8.5))
ax2 = ax.twinx()

group_base_colors = ['#b0b35a', '#f39851', '#e65050', '#3572ef', '#7b5bb1']
markers = ['D', 's', 'o', '^', '*', 'x']
interfaces = ['/homepage', '/product1', '/product2', '/cart', '/pay']
input_dir = [f"actual workload/{api}.csv" for api in ['homepage', 'product1', 'product2', 'cart', 'pay']]

# Data containers for actual and quantified workloads
X, Y = [], []

# Load and normalize actual workload data
for path in input_dir:
    if os.path.exists(path):
        df = pd.read_csv(path)
        X.append(df['workload'] / 20)

# Load latency data for quantified workload
q_file = "quantified workload/avg latency HTTP 500.csv"
if os.path.exists(q_file):
    df_q = pd.read_csv(q_file)
    for i in interfaces:
        Y.append(df_q[i])

def analyze_spearman(X_res, Y_raw, max_lag=6):
    # Calculate Spearman correlation with time lags
    corrs = []
    lags = range(-max_lag, 0)
    for lag in lags:
        x_slice = X_res[:len(Y_raw) + lag]
        y_slice = Y_raw[-lag:]
        min_len = min(len(x_slice), len(y_slice))
        corr, _ = spearmanr(x_slice[:min_len], y_slice[:min_len])
        corrs.append(corr if min_len > 1 else 0)
    best_corr = max(corrs, key=abs)
    return lags[corrs.index(best_corr)], best_corr

def analyze_pearson(X_res, Y_raw, max_lag=6):
    # Calculate Pearson correlation with time lags
    corrs = []
    lags = range(-max_lag, 0)
    for lag in lags:
        x_slice = X_res[:len(Y_raw) + lag]
        y_slice = Y_raw[-lag:]
        min_len = min(len(x_slice), len(y_slice))
        corr = np.corrcoef(x_slice[:min_len], y_slice[:min_len])[0, 1] if min_len > 1 else 0
        corrs.append(corr)
    best_corr = max(corrs, key=abs)
    return lags[corrs.index(best_corr)], best_corr

# Execute cross-correlation analysis with resampling
corr_results = []
for X_sub, Y_sub in zip(X, Y):
    x_indices = np.linspace(0, len(X_sub) - 1, len(Y_sub))
    X_resampled = interp1d(np.arange(len(X_sub)), X_sub, kind='linear')(x_indices)
    
    lag_p, c_p = analyze_pearson(X_resampled, Y_sub)
    lag_s, c_s = analyze_spearman(X_resampled, Y_sub)
    corr_results.append({'p': c_p, 's': c_s, 'lp': lag_p, 'ls': lag_s})

# Plot Actual Workload on primary Y-axis
for i in range(5):
    if os.path.exists(input_dir[i]):
        df = pd.read_csv(input_dir[i])
        uc = df['workload'] / 20
        x_axis = np.linspace(0, 60, len(uc))
        ax.plot(x_axis, uc, alpha=0.2, label=interfaces[i], color=group_base_colors[i])

ax.set_xlabel('Time (min)', fontsize=32, fontweight='bold')
ax.set_ylabel('Actual workload (AOL = 1s)', fontsize=32, fontweight='bold')
ax.tick_params(axis='both', labelsize=28)
ax.set_ylim(20, 100)

# Plot Quantified Latency on secondary Y-axis
df_q_plot = pd.read_csv(q_file).fillna(0)
for index, i in enumerate(interfaces):
    uc_q = df_q_plot[i].to_numpy()
    x_axis_q = np.linspace(0, 60, len(uc_q))
    ax2.plot(x_axis_q, uc_q, label=i, color=group_base_colors[index], 
             linewidth=1.5, marker=markers[index], markevery=15,
             markersize=7 if markers[index] in ['*', 'x'] else 5)

ax2.set_ylabel('Latency HTTP 500 (ms)', fontsize=32, fontweight='bold')
ax2.tick_params(axis='y', labelsize=28)

# Legend alignment and formatting
leg1 = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.988), ncol=5, frameon=False, 
                fontsize=28, handletextpad=0.5, columnspacing=1.0)
for text in leg1.get_texts(): text.set_alpha(0)
ax.add_artist(leg1)

leg2 = ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=5, frameon=False, 
                 fontsize=28, handletextpad=0.5, columnspacing=1.0)
for text in leg2.get_texts(): text.set_position((0, -10))

ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.savefig("fig_latency_HTTP_500_vs_workload.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()