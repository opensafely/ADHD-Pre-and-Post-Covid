import os
import pandas as pd
import numpy as np

from table_wrangle_functions import (
    add_datestamp
)

# Ensure the 'outputs' directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load the data
adhd_medication_data = pd.read_csv("output/Patient_table_3_rolling_6month_incident.csv.gz")

# getting the month and year only
adhd_medication_data['last_mph_med_date'] = (
    pd.to_datetime(adhd_medication_data['last_mph_med_date'], format='%Y-%m-%d')
)

adhd_medication_data['last_mph_med_date_month_date'] = (
    adhd_medication_data['last_mph_med_date'].apply(lambda x: x.strftime('%Y-%m'))
)


# # #Adding a small number suprresion
# rounding_unit = 10
# output['size'] = np.ceil(output['size'] / rounding_unit)
# output['size'] = output['size'] * rounding_unit

# # #Adding a set time stamp
# output['timestamp'] = add_datestamp()

# # Saving the table
# output.to_csv("output/Table_5_time_from_diagnosis_to_treatment.csv")

