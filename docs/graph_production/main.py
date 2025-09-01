import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import dia_plots, nhs_palette, user_time_plots
import utils 

"""
Ploting measures
"""
# Loading 
ADHD_dia_data = pd.read_csv(dia_plots['file_path'])

# Spliting the data
sex_group, age_group, age_group_young, age_group_middle, age_group_old = utils.get_sex_and_age_groups(ADHD_dia_data)

#Ploting the data 
fig, axes = utils.plot_adhd_prevalence_charts(sex_group, age_group_young, age_group_middle, age_group_old)
axes[0, 0].set_title(dia_plots['top_left']['title'])
axes[0, 1].set_title(dia_plots['top_right']['title'])
axes[1, 0].set_title(dia_plots['bottom_left']['title'])
axes[1, 1].set_title(dia_plots['bottom_right']['title'])

axes = utils.watermark_plot(axes,dia_plots['watermark'])

fig.savefig(dia_plots['file_name'], format="jpeg", dpi=300)

"""
Ploting user defining tables
"""

time_between_dia_and_med = pd.read_csv(user_time_plots['file_path'])



# Usage
fig, axes = plot_time_from_diagnosis_to_medication(time_between_dia_and_med, nhs_palette)

fig.savefig("Table_5_time_from_diagnosis_to_treatment.jpeg", format="jpeg", dpi=300)