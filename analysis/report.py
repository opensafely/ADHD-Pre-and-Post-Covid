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

#Computing ADHD disgnosis 

adhd_total_sex_table = data.groupby(['sex']).count()
adhd_total_sex_table = adhd_total_sex_table.drop(['patient_id'],axis=1)

adhd_dia_sex_table = data.