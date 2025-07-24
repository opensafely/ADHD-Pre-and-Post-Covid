import pandas as pd
import requests

url = "https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv"
file_path = "docs/emis_calculation/LD_data.csv"
groupby_index = ['YEAR','SEX','AGE_BAND']
adhd_code = ['LDOB089','LDOB091']


df_emis = pd.read_csv(url)

response = requests.get(url)

with open(file_path, "wb") as f:
    f.write(response.content)

# Read the CSV file into a Pandas DataFrame
ld_data_adhd = pd.read_csv(file_path)

# Need to filter the codes LDOB089 and LDOB091
adhd_counts = ld_data_adhd[ld_data_adhd['INDICATOR'].isin(adhd_code)]

#Need to sum over
adhd_counts = adhd_counts.groupby(groupby_index, as_index=False)['VALUE'].sum()

adhd_counts