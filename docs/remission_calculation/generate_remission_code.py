import pandas as pd
import requests
from config import config
import os


#Downloading the file
url = config['SNOMED_code_usage_2023_24']
response = requests.get(url)
filename = config['file_path_to_save'] + os.path.basename(url)

with open(filename, "wb") as f:
    f.write(response.content)

#Getting the data
table = pd.read_excel(filename)

adhdrem_codelist = pd.read_csv('codelists/nhsd-primary-care-domain-refsets-adhdrem_cod.csv')
adhdrem_codelist = adhdrem_codelist[config['SNOMED_Concept_ID']]
remission_table = table[table[config['SNOMED_Concept_ID']].isin(adhdrem_codelist)]

remission_table