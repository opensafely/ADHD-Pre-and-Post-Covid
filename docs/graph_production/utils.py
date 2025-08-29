import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.ticker as mtick
import matplotlib.transforms as transforms

from config import nhs_palette

#For single year 
def single_year_table(table):

    table = table[['ratio','sex','age_band']]
    table = table[~table['ratio'].isnull()]

    table = pd.pivot_table(table, values='ratio', index=['age_band'], columns=['sex'] )

    return table

def grouped_by_demographics(table, demo, cols_to_sum = ['numerator','denominator'], 
                            year_col = ['interval_start']):

    #Need to sum over
    combine_cols = year_col + [demo]

    output = table.groupby(combine_cols, as_index = False)[cols_to_sum].sum()

    #Computing the ratio
    output['ratio'] = output[cols_to_sum[0]]/output[cols_to_sum[1]]

    #Covert into percentage
    output['ratio'] = output['ratio']*100

    return output


def grouped_by_overall(table, cols_to_sum = ['numerator','denominator'], 
                            year_col = ['interval_start']):

    #Need to sum over
    combine_cols = year_col

    output = table.groupby(combine_cols, as_index = False)[cols_to_sum].sum()

    #Computing the ratio
    output['ratio'] = output[cols_to_sum[0]]/output[cols_to_sum[1]]

    #Covert into percentage
    output['ratio'] = output['ratio']*100

    return output

def plot_adhd_prevalence_charts(sex_group, age_group_young, age_group_middle, age_group_old, nhs_palette = nhs_palette ):
    fig, axes = plt.subplots(2, 2, figsize=(15.7, 15.3))  # A4 landscape in inches

    # By sex
    sns.lineplot(x="interval_start", y="ratio", hue="sex", data=sex_group, ax=axes[0, 0], palette=nhs_palette)
    axes[0, 0].set_ylabel("Prevalence, %")
    axes[0, 0].set_xlabel("Year")
    ax_tmp0 = axes[0, 0].twinx()
    sns.barplot(x="interval_start", y="numerator", hue="sex", ax=ax_tmp0, data=sex_group, palette=nhs_palette, alpha=0.3, dodge=True)
    ax_tmp0.set_ylabel("Count")
    axes[0, 0].set_title("ADHD Prevalence and Counts by Sex")
    axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=90)
    #axes[0, 0].get_legend().remove()
    handles1, labels1 = axes[0, 0].get_legend_handles_labels()
    handles2, labels2 = ax_tmp0.get_legend_handles_labels()
    axes[0, 0].legend((*handles1, *handles2), (*len(labels1)*[''], *labels2),
             loc='best', ncol=2, handlelength=3, edgecolor='black', handletextpad = 0.1,
             labelspacing = 0.1, columnspacing = 0.1,
)
    ax_tmp0.get_legend().remove()

    # Young age bands
    sns.lineplot(x="interval_start", y="ratio", hue="age_band", data=age_group_young, ax=axes[0, 1], palette=nhs_palette)
    axes[0, 1].set_ylabel("Prevalence, %")
    axes[0, 1].set_xlabel("Year")
    ax_tmp1 = axes[0, 1].twinx()
    sns.barplot(x="interval_start", y="numerator", hue="age_band", ax=ax_tmp1, data=age_group_young, palette=nhs_palette, alpha=0.3, dodge=True)
    ax_tmp1.set_ylabel("Count")
    axes[0, 1].set_title("ADHD Prevalence and Counts by Age Band (Young)")
    axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=90)
    #axes[0, 0].get_legend().remove()
    handles1, labels1 = axes[0, 1].get_legend_handles_labels()
    handles2, labels2 = ax_tmp1.get_legend_handles_labels()
    axes[0, 1].legend((*handles1, *handles2), (*len(labels1)*[''], *labels2),
             loc='best', ncol=2, handlelength=3, edgecolor='black',handletextpad = 0.1,
             labelspacing = 0.1, columnspacing = 0.1
)
    ax_tmp1.get_legend().remove()

    # Middle age bands
    sns.lineplot(x="interval_start", y="ratio", hue="age_band", data=age_group_middle, ax=axes[1, 0], palette=nhs_palette)
    axes[1, 0].set_ylabel("Prevalence, %")
    axes[1, 0].set_xlabel("Year")
    ax_tmp2 = axes[1, 0].twinx()
    sns.barplot(x="interval_start", y="numerator", hue="age_band", ax=ax_tmp2, data=age_group_middle, palette=nhs_palette, alpha=0.3, dodge=True)
    ax_tmp2.set_ylabel("Count")
    axes[1, 0].set_title("ADHD Prevalence and Counts by Age Band (Middle Age)")
    axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=90)

    handles1, labels1 = axes[1, 0].get_legend_handles_labels()
    handles2, labels2 = ax_tmp2.get_legend_handles_labels()
    axes[1, 0].legend((*handles1, *handles2), (*len(labels1)*[''], *labels2),
             loc='best', ncol=2, handlelength=3, edgecolor='black',handletextpad = 0.1,
             labelspacing = 0.1, columnspacing = 0.1
)
    ax_tmp2.get_legend().remove()

    # Old age bands
    sns.lineplot(x="interval_start", y="ratio", hue="age_band", data=age_group_old, ax=axes[1, 1], palette=nhs_palette)
    axes[1, 1].set_ylabel("Prevalence, %")
    axes[1, 1].set_xlabel("Year")
    ax_tmp3 = axes[1, 1].twinx()
    sns.barplot(x="interval_start", y="numerator", hue="age_band", ax=ax_tmp3, data=age_group_old, palette=nhs_palette, alpha=0.3, dodge=True)
    ax_tmp3.set_ylabel("Count")
    axes[1, 1].set_title("ADHD Prevalence and Counts by Age Band (Retired)")
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=90)
    handles1, labels1 = axes[1, 1].get_legend_handles_labels()
    handles2, labels2 = ax_tmp3.get_legend_handles_labels()
    axes[1, 1].legend((*handles1, *handles2), (*len(labels1)*[''], *labels2),
             loc='best', ncol=2, handlelength=3, edgecolor='black',handletextpad = 0.1,
             labelspacing = 0.1, columnspacing = 0.1
)
    ax_tmp3.get_legend().remove()

    plt.tight_layout()

    #plt.subplots_adjust(hspace=1.75)
    return fig, axes

def get_sex_and_age_groups(table):
    sex_group = grouped_by_demographics(table, 'sex')
    age_group = grouped_by_demographics(table, 'age_band')
    age_group_young = age_group[age_group['age_band'].isin(['0 to 9', '10 to 17', '18 to 24'])]
    age_group_middle = age_group[age_group['age_band'].isin(['25 to 34', '35 to 44', '45 to 54', '55 to 64'])]
    age_group_old = age_group[age_group['age_band'].isin(['65 to 74', '75 and over'])]
    return sex_group, age_group, age_group_young, age_group_middle, age_group_old



