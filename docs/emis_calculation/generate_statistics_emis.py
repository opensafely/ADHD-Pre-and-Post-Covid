import pandas as pd
import requests
from config import config
import os
import zipfile

# Need to save the data
keys_in_config_dict = list(config.keys())
url_keys = [x for x in keys_in_config_dict if ('url' in x)]

for each_url_key in url_keys:
    url = config[each_url_key]
    response = requests.get(url)
    print(each_url_key)
    filename = config['file_path_to_save'] + os.path.basename(url)
    with open(filename, "wb") as f:
        f.write(response.content)

zip_files = [f for f in os.listdir(config['file_path_to_save']) if f.endswith('.zip')]

for each_zip_file in zip_files:
    zip_path = os.path.join(config['file_path_to_save'], each_zip_file)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(config['file_path_to_save'])


print('done')
# df_emis = pd.read_csv(url)

# response = requests.get(url)

# with open(file_path, "wb") as f:
#     f.write(response.content)

# # Read the CSV file into a Pandas DataFrame
# ld_data_adhd = pd.read_csv(file_path)
# ld_data_adhd['SEX'] = ld_data_adhd['SEX'].replace(sex_rename)

# # Need to filter the codes LDOB089 and LDOB091
# adhd_counts = ld_data_adhd[ld_data_adhd['INDICATOR'].isin(adhd_code)]
# all_counts = ld_data_adhd[ld_data_adhd['INDICATOR'].isin(all_code)]

# #Need to sum over
# adhd_counts = adhd_counts.groupby(groupby_index, as_index=False)['VALUE'].sum()
# all_counts = all_counts.groupby(groupby_index, as_index=False)['VALUE'].sum()

# #Need to some renaming
# adhd_counts = adhd_counts.rename(columns={'VALUE': 'numerator'})
# all_counts = all_counts.rename(columns={'VALUE': 'denominator'})

# print(all_counts)