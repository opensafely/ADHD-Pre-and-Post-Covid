

config = {
    'url_2324':"https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv",
    'url_2223':"https://files.digital.nhs.uk/43/BD15AC/health_care_ld_sicbl_2022-23.csv",
    'url_1722':"https://files.digital.nhs.uk/49/70A43E/health_care_ld_ccg_data_1617_2021.zip",
    'url_1621':"https://files.digital.nhs.uk/49/70A43E/health_care_ld_ccg_data_1617_2021.zip",
    'file_path_to_save':"docs/emis_calculation/",
    "groupby_index":['YEAR','SEX','AGE_BAND'],
    'numerator' : ['LDOB089','LDOB091'],
    'denominator' : ['LDOB003A' , 'LDOB003B'],
    'all_code' : ['ALL'],
    'sex_rename' : {'F':'female' , 'M':'male'}
    }
