import pandas as pd
from scipy import stats

# Load the txt file with encoding=Gb18030


times=["201906","202006","202106","202206","202306","202406"]

for time in times:
    file_path = f'./{time}_modified_new.txt'  # Update with the actual file path
    df = pd.read_csv(file_path, encoding='GB18030', delimiter='\t')

    # Separate worse_SE by gender
    rural_worse_SE = df[df['城市/乡镇列'] == 1]['worse_SE']
    city_worse_SE = df[df['城市/乡镇列'] == 2]['worse_SE']

    # Calculate mean and standard deviation
    rural_mean = rural_worse_SE.mean()
    rural_std = rural_worse_SE.std()
    city_mean = city_worse_SE.mean()
    city_std = city_worse_SE.std()

    print(f"{time}-rural worse_SE: {rural_mean:.2f} ± {rural_std:.2f}")
    print(f"{time}-city worse_SE: {city_mean:.2f} ± {city_std:.2f}")

    # Perform normality test (Shapiro-Wilk Test)
    rural_normality = stats.shapiro(rural_worse_SE)
    city_normality = stats.shapiro(city_worse_SE)

    print(f"{time}-rural Shapiro-Wilk test: statistic={rural_normality.statistic:.4f}, p-value={rural_normality.pvalue:.4f}")
    print(f"{time}-city Shapiro-Wilk test: statistic={city_normality.statistic:.4f}, p-value={city_normality.pvalue:.4f}")

    # Check if both distributions are normal (p-value > 0.05)
    if rural_normality.pvalue > 0.05 and city_normality.pvalue > 0.05:
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(rural_worse_SE, city_worse_SE, equal_var=False)
        print(f"t-statistic: {t_stat:.4f}")
        print(f"p-value: {p_value:.4f}")
    else:
        # Perform Mann-Whitney U test as data is not normally distributed
        u_stat, u_p_value = stats.mannwhitneyu(rural_worse_SE, city_worse_SE, alternative='two-sided')
        print(f"Mann-Whitney U test: U-statistic={u_stat:.4f}, p-value={u_p_value:.4f}")

