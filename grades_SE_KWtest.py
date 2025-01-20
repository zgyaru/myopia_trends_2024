import pandas as pd
from scipy.stats import kruskal
import scikit_posthocs as sp

# 定义时间段
times = ["201906", "202006", "202106", "202206", "202306", "202406"]

# 创建一个空的DataFrame来存储所有数据
all_data = pd.DataFrame()

# 读取数据并合并
for time in times:
    file_path = f'./{time}_modified_new.txt'
    df = pd.read_csv(file_path, encoding='GB18030', delimiter='\t')
    df['time'] = time  # 添加一列以区分时间段
    all_data = pd.concat([all_data, df], ignore_index=True)

# 提取各时间段的worse_SE数据
data_dict = {time: all_data[all_data['time'] == time]['worse_SE'].dropna().astype(float) for time in times}

# 提取所有时间段的worse_SE数据
worse_SE_values = [data_dict[time] for time in times]

# 进行Kruskal-Wallis H检验
kruskal_result = kruskal(*worse_SE_values)

print(f"Kruskal-Wallis H检验结果: H值 = {kruskal_result.statistic}, p值 = {kruskal_result.pvalue}")

# 如果Kruskal-Wallis H检验结果显著（p值 < 0.05），进行成对比较（Dunn检验）
if kruskal_result.pvalue < 0.05:
    # 创建一个包含所有数据的长格式DataFram
    long_format_data = pd.DataFrame({
        'worse_SE': pd.concat(worse_SE_values),
        'time': sum([[time] * len(data_dict[time]) for time in times], [])
    })

    # 进行Dunn检验并调整p值
    dunn_result = sp.posthoc_dunn(long_format_data, val_col='worse_SE', group_col='time', p_adjust='bonferroni')
    print("Dunn检验结果（调整后的p值）：")
    print(dunn_result)
else:
    print("Kruskal-Wallis H检验结果不显著，无需进行成对比较。")
