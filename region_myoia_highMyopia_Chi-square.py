import pandas as pd
from scipy import stats

# 时间点列表
times = ["201906", "202006", "202106", "202206", "202306", "202406"]

for time in times:
    file_path = f'./{time}_modified_new.txt'  # 更新实际文件路径
    df = pd.read_csv(file_path, encoding='GB18030', delimiter='\t')
    
    # 近视（1, 2, 3表示近视，3表示高度近视）
    df['myopia'] = df['worse_check_result'].apply(lambda x: 1 if x in [1, 2, 3] else 0)
    df['high_myopia'] = df['worse_check_result'].apply(lambda x: 1 if x == 3 else 0)
    
    # 分别计算城乡近视率
    rural_myopia_rate = df[df['城市/乡镇列'] == 1]['myopia'].mean()
    urban_myopia_rate = df[df['城市/乡镇列'] == 2]['myopia'].mean()
    rural_high_myopia_rate = df[df['城市/乡镇列'] == 1]['high_myopia'].mean()
    urban_high_myopia_rate = df[df['城市/乡镇列'] == 2]['high_myopia'].mean()
    
    print(f"{time}-Rural Myopia Rate: {rural_myopia_rate:.4f}")
    print(f"{time}-Urban Myopia Rate: {urban_myopia_rate:.4f}")
    print(f"{time}-Rural High Myopia Rate: {rural_high_myopia_rate:.4f}")
    print(f"{time}-Urban High Myopia Rate: {urban_high_myopia_rate:.4f}")
    
    # 构建频率表
    contingency_table_myopia = pd.crosstab(df['城市/乡镇列'], df['myopia'])
    contingency_table_high_myopia = pd.crosstab(df['城市/乡镇列'], df['high_myopia'])
    
    # 进行卡方检验（Chi-square test）
    chi2_myopia, p_myopia, _, _ = stats.chi2_contingency(contingency_table_myopia)
    chi2_high_myopia, p_high_myopia, _, _ = stats.chi2_contingency(contingency_table_high_myopia)
    
    print(f"{time}-Chi-square test for Myopia: chi2={chi2_myopia:.4f}, p-value={p_myopia:.4f}")
    print(f"{time}-Chi-square test for High Myopia: chi2={chi2_high_myopia:.4f}, p-value={p_high_myopia:.4f}")

    print("\n")
