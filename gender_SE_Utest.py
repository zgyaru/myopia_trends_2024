

#矫正了年级后男女u检验
import pandas as pd
from scipy import stats

# Load the txt file with encoding=Gb18030
times = ["201906", "202006", "202106", "202206", "202306", "202406"]
grades = list(range(1, 13))  # Year grades from 1 to 12

for time in times:
    file_path = f'./{time}_modified_new.txt'  # Update with the actual file path
    df = pd.read_csv(file_path, encoding='GB18030', delimiter='\t')

    # Combine all grades together for overall analysis
    male_worse_SE_corrected = df[df['studentSex'] == 0]['worse_SE_corrected']
    female_worse_SE_corrected = df[df['studentSex'] == 1]['worse_SE_corrected']

    if male_worse_SE_corrected.empty or female_worse_SE_corrected.empty:
        print(f"{time}: Insufficient data for one or both genders")
        continue

    # Calculate mean and standard deviation
    male_mean = male_worse_SE_corrected.mean()
    male_std = male_worse_SE_corrected.std()
    female_mean = female_worse_SE_corrected.mean()
    female_std = female_worse_SE_corrected.std()

    print(f"{time} - Overall - Male worse_SE_corrected: {male_mean:.2f} ± {male_std:.2f}")
    print(f"{time} - Overall - Female worse_SE_corrected: {female_mean:.2f} ± {female_std:.2f}")

    # Perform normality test (Shapiro-Wilk Test)
    male_normality = stats.shapiro(male_worse_SE_corrected)
    female_normality = stats.shapiro(female_worse_SE_corrected)

    print(f"{time} - Overall - Male Shapiro-Wilk test: statistic={male_normality.statistic:.4f}, p-value={male_normality.pvalue:.4f}")
    print(f"{time} - Overall - Female Shapiro-Wilk test: statistic={female_normality.statistic:.4f}, p-value={female_normality.pvalue:.4f}")

    # Check if both distributions are normal (p-value > 0.05)
    if male_normality.pvalue > 0.05 and female_normality.pvalue > 0.05:
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(male_worse_SE_corrected, female_worse_SE_corrected, equal_var=False)
        print(f"t-statistic: {t_stat:.4f}")
        print(f"p-value: {p_value:.4f}")
    else:
        # Perform Mann-Whitney U test as data is not normally distributed
        u_stat, u_p_value = stats.mannwhitneyu(male_worse_SE_corrected, female_worse_SE_corrected, alternative='two-sided')
        print(f"Mann-Whitney U test: U-statistic={u_stat:.4f}, p-value={u_p_value:.4f}")



