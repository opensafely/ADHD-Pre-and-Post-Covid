import os
import pandas as pd
import numpy as np

# Ensure the 'outputs' directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load the data
adhd_data = pd.read_csv("output/adhd_dataset.csv.gz")

week_bin = [0, 1, 2, 4, 8, 12, 21, 52, 104]

# Placing into a histogram
output = adhd_data["times_between_dia_med_weeks"].value_counts(bins=week_bin)

# Need to label the outputs
output = output.rename_axis("FAKE_DATA_weeks_between_dx_and_med_date")
output = output.rename("FAKE_DATA_counts")

# Small number supppression
rounding_unit = 10
output = np.ceil((output / rounding_unit))
output = output * rounding_unit

# Saving the table
output.to_csv("output/adhd_dia_med_gap_weeks.csv")
