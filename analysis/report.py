import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ensure the 'outputs' directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load the data
data = pd.read_csv("output/full_dataset.csv.gz")

# Melt the ADHD events data
adhd_events = data.melt(
    id_vars=['patient_id', 'sex'],
    value_vars=[f'num_adhd_events_{year}' for year in range(2016, 2024)],
    var_name='year',
    value_name='num_adhd_events'
)

# Extract the year from the 'year' column
adhd_events['year'] = adhd_events['year'].str.extract(r'(\d{4})').astype(int)

# Group by year and sex, then sum the number of ADHD events
adhd_events_grouped = adhd_events.groupby(['year', 'sex'])['num_adhd_events'].sum().reset_index()

# Plot the ADHD events per year, per sex
plt.figure(figsize=(12, 6))
width = 0.35
years = adhd_events_grouped['year'].unique()
x = np.arange(len(years))

for i, sex in enumerate(adhd_events_grouped['sex'].unique()):
    subset = adhd_events_grouped[adhd_events_grouped['sex'] == sex]
    plt.bar(x + (i * width - width / 2), subset['num_adhd_events'], width, label=sex)

plt.xlabel('Year')
plt.ylabel('Number of ADHD Events')
plt.title('Number of ADHD Events per Year by Sex')
plt.xticks(x, years)
plt.legend(title='Sex')
plt.grid(True, axis='y')
plt.savefig(os.path.join(output_dir, 'adhd_events_per_year_by_sex.png'))
plt.close()

# Melt the methylphenidate prescription data
methylphenidate_prescriptions = data.melt(
    id_vars=['patient_id', 'sex'],
    value_vars=[f'num_methylphenidate_prescription_{year}' for year in range(2016, 2024)],
    var_name='year',
    value_name='num_methylphenidate_prescriptions'
)

# Extract the year from the 'year' column
methylphenidate_prescriptions['year'] = methylphenidate_prescriptions['year'].str.extract(r'(\d{4})').astype(int)

# Group by year and sex, then sum the number of methylphenidate prescriptions
methylphenidate_prescriptions_grouped = methylphenidate_prescriptions.groupby(['year', 'sex'])['num_methylphenidate_prescriptions'].sum().reset_index()

# Plot the methylphenidate prescriptions per year, per sex
plt.figure(figsize=(12, 6))
for i, sex in enumerate(methylphenidate_prescriptions_grouped['sex'].unique()):
    subset = methylphenidate_prescriptions_grouped[methylphenidate_prescriptions_grouped['sex'] == sex]
    plt.bar(x + (i * width - width / 2), subset['num_methylphenidate_prescriptions'], width, label=sex)

plt.xlabel('Year')
plt.ylabel('Number of Methylphenidate Prescriptions')
plt.title('Number of Methylphenidate Prescriptions per Year by Sex')
plt.xticks(x, years)
plt.legend(title='Sex')
plt.grid(True, axis='y')
plt.savefig(os.path.join(output_dir, 'methylphenidate_prescriptions_per_year_by_sex.png'))
plt.close()
