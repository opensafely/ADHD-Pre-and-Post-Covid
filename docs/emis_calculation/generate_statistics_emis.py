import pandas as pd
import requests
from config import config
import os
import zipfile
import utils

# This function downloads the files
utils.create_source_files_from_nhs_england(config)

dict_of_files = config['list_of_csv']

for each_key in list(dict_of_files.keys()):

    #opening each file
    each_csv = pd.read_csv(config['file_path_to_save'] + dict_of_files[each_key])
    
    #Wrangle the file to match OS's outputs

    #Getting the correct cols
    each_csv = each_csv[config['cols_of_interest']]

    #Rename the Sex col
    each_csv[config['nhs_sex_col']] = each_csv[config['nhs_sex_col']].replace(config['sex_rename'])

    #Computing the ratio
    each_adhd_counts = each_csv[each_csv[config['nhs_indicator_col']].isin(config['numerator'])]
    each_all_counts = each_csv[each_csv[config['nhs_indicator_col']].isin(config['denominator'])]

    each_adhd_counts = each_adhd_counts.groupby(config['groupby_index'], as_index=False)[config['nhs_vaule_col']].sum()
    each_adhd_counts = each_adhd_counts.rename(columns=config['rename_col_for_numerator'])
    each_all_counts = each_all_counts.groupby(config['groupby_index'], as_index=False)[config['nhs_vaule_col']].sum()
    each_all_counts = each_all_counts.rename(columns=config['rename_col_for_denominator'])

    #Join
    each_ratio = pd.merge(each_adhd_counts, each_all_counts, on=config['groupby_index'])
    each_ratio = each_ratio.rename(columns=config['raname_cols_indices'])

    #Computing the ratio
    each_ratio[config['nhs_ratio_col']] = each_ratio[config['nhs_numerator_col']]/each_ratio[config['nhs_denominator_col']]
    
    #Need to set out the year

    print(each_ratio)


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