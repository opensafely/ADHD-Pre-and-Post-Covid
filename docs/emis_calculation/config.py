

config = {
    'url_2324':"https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv",
    'url_2223':"https://files.digital.nhs.uk/43/BD15AC/health_care_ld_sicbl_2022-23.csv",
    }

url = "https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv"
file_path = "docs/emis_calculation/LD_data.csv"

groupby_index = ['YEAR','SEX','AGE_BAND']

adhd_code = ['LDOB089','LDOB091']

deoinator = ['LDOB003A' , 'LDOB003B']

all_code = ['ALL']

sex_rename = {'F':'female' , 'M':'male'}