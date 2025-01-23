import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ensure the 'outputs' directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load the data
adhd_data = pd.read_csv("output/adhd_dataset.csv.gz")

week_bin = [0,1,2,4,8,12,21,52,104]

output = adhd_data['times_between_dia_med_weeks'].value_counts(bins = week_bin)

print(output)