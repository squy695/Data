import pandas as pd
import numpy as np
import os

# 设置随机种子以确保可重复性
np.random.seed(42)

# 读取原始 CSV 文件
df = pd.read_csv('locust/wiki/wiki.csv')

# 获取总行数
n = len(df)

# 生成 5 个新的 CSV 文件，每个文件的第一行为对应的1/5分位点行
for i in range(1, 9):
    # 计算第 i 个 1/5 分位点的位置（向下取整）
    index = int(n * (i / 9)) if i < 9 else n - 1  # 避免 index 超出范围

    df_reordered = pd.concat([df.iloc[index:], df.iloc[:index]]).reset_index(drop=True)
    
    output_filename = f'wiki {i}.csv'
    df_reordered.to_csv(output_filename, index=False)
