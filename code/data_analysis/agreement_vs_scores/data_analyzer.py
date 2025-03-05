# Combine all steps from unzipping to plotting into a single script

import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
import json

unzip_dir = 'data/'

def common_language_effect_size(x, y, u): # https://en.wikipedia.org/wiki/Mann–Whitney_U_test#Effect_sizes
    return u / (len(x) * len(y))

def rank_biserial_correlation(x, y, u): # https://en.wikipedia.org/wiki/Mann–Whitney_U_test#Effect_sizes
    return 1 - 2 * common_language_effect_size(x, y, u)

# Load CSV files into dataframes
csv_files = ['Credit_Approval_System.csv', 'Medical_Expenditure_System.csv']
dfs = {}

for csv_file in csv_files:
    dfs[csv_file[:-4].replace('_',' ')] = pd.read_csv(unzip_dir + csv_file)

# Perform Mann-Whitney U tests
mwu_results = {}

for df_name in dfs.keys():
    dfs[df_name] = dfs[df_name].rename(columns={'Compliance Score': 'Explanatory Relevance', 'Max Confidence': 'Confidence', 'Average DoX': 'DoX'})


for df_name, df in dfs.items():
    mwu_results[df_name] = {}
    for col in ["DoX", "Confidence", "Explanatory Relevance"]:
        group_Y = df[df['Interpersonal Agreement'] == 'Y'][col]
        group_N = df[df['Interpersonal Agreement'] == 'N'][col]
        u_stat, p_value = mannwhitneyu(group_Y, group_N, alternative='greater')
        mwu_results[df_name][col] = {'U_statistic': u_stat, 'p_value': p_value, 'common_language_effect_size': common_language_effect_size(group_Y,group_N,u_stat), 'rank_biserial_correlation': rank_biserial_correlation(group_Y,group_N,u_stat)}

dfs_values = list(dfs.values())
merged_df = dfs_values[0]
for d in dfs_values[1:]:
    merged_df = merged_df.append(d)
mwu_results['All'] = {}
for col in ["DoX", "Confidence", "Explanatory Relevance"]:
    group_Y = merged_df[merged_df['Interpersonal Agreement'] == 'Y'][col]
    group_N = merged_df[merged_df['Interpersonal Agreement'] == 'N'][col]
    u_stat, p_value = mannwhitneyu(group_Y, group_N, alternative='greater')
    effect_size = 1 - (2 * u_stat) / (len(group_Y) * len(group_N))  # Compute rank-biserial correlation
    mwu_results['All'][col] = {'U_statistic': u_stat, 'p_value': p_value, 'common_language_effect_size': common_language_effect_size(group_Y,group_N,u_stat), 'rank_biserial_correlation': rank_biserial_correlation(group_Y,group_N,u_stat)}
dfs['All'] = merged_df

print(json.dumps(mwu_results, indent=4))

# Plot juxtaposed boxplots with corrected labels and p-value positions
plt.rcParams.update({'font.size': 14, "axes.labelsize": 14})  # Increase global font size
fig, axes = plt.subplots(1, 3, figsize=(11, 6))

for ax, (df_name, df) in zip(axes, dfs.items()):
    df['Interpersonal Agreement'] = df['Interpersonal Agreement'].replace({'N': 'Disagreement', 'Y': 'Agreement'})
    ax.set_title(df_name)
    df_melted = df.melt(id_vars=['Interpersonal Agreement'], value_vars=["DoX", "Confidence", "Explanatory Relevance"])
    df_melted['variable'].replace({'Confidence': 'Prt'}, inplace=True)
    df_melted['variable'].replace({'Explanatory Relevance': 'DoX*Prt'}, inplace=True)
    sns.boxplot(x="variable", y="value", hue="Interpersonal Agreement", data=df_melted, hue_order=['Disagreement', 'Agreement'], ax=ax)
    ax.set_xlabel("")
    if df_name != 'Credit Approval System':
        ax.set_ylabel("")
    
    for i, col in enumerate(["DoX", "Confidence", "Explanatory Relevance"]):
        p_value = mwu_results[df_name][col]['p_value']
        if col == "DoX":
            position = df[df['Interpersonal Agreement'] == 'Disagreement'][col].min() * 0.85
        else:
            position = df[col].max() * 1.05

        ax.annotate(f'p: {p_value:.3f}', xy=(i, position), xytext=(i, position), 
                    textcoords="data", ha='center', va='center', fontsize=14, color='red')
        if df_name!='All':
            ax.legend().remove()

plt.tight_layout()
plt.savefig(f'agreement_vs_scores.png')
