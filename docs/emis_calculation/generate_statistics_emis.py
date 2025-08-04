import pandas as pd
import requests
from config import config
import os
import zipfile
import utils

# Check if any required CSV file is missing, then download if needed
missing_files = [
    fname for fname in config['list_of_csv'].values()
    if not os.path.isfile(os.path.join(config['file_path_to_save'], fname))
]
if missing_files:
    utils.create_source_files_from_nhs_england(config)

dict_of_files = config['list_of_csv']

for each_key in list(dict_of_files.keys()):

    #opening each file
    each_csv = pd.read_csv(config['file_path_to_save'] + dict_of_files[each_key])
    
    #Wrangle the file to match OS's outputs
    each_ratio = utils.wrangling_table_to_opensafely_form(each_csv,each_key,config)



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