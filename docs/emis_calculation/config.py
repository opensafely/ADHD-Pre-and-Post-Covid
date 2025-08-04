

config = {
    'url_2324':"https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv",
    'url_2223':"https://files.digital.nhs.uk/43/BD15AC/health_care_ld_sicbl_2022-23.csv",
    'url_1722':"https://files.digital.nhs.uk/BC/016738/health_care_ld_sicbl_data_1718_2122.zip",
    'url_1621':"https://files.digital.nhs.uk/49/70A43E/health_care_ld_ccg_data_1617_2021.zip",
    'main_link': "https://digital.nhs.uk/data-and-information/publications/statistical/health-and-care-of-people-with-learning-disabilities",
    'file_path_to_save': "docs/emis_calculation/",
    'list_of_csv':{
        '23_24':'health_care_ld_sicbl_2023-24.csv',
        '22_23':'health_care_ld_sicbl_2022-23.csv',
        '21_22':'Health and Care of People with Learning Disabilities SICBL data 2021-22.csv',
        '20_21':'Health and Care of People with Learning Disabilities SICBL data 2020-21.csv',
        '19_20':'Health and Care of People with Learning Disabilities SICBL data 2019-20.csv',
        '18_19':'Health and Care of People with Learning Disabilities SICBL data 2018-19.csv',
        '17_18':'Health and Care of People with Learning Disabilities SICBL data 2017-18.csv',
        '16_17':'Health and Care of People with Learning Disabilities CCG data 2016-17.csv'
    }
    "groupby_index":['YEAR','SEX','AGE_BAND'],
    'numerator' : ['LDOB089','LDOB091'],
    'denominator' : ['LDOB003A' , 'LDOB003B'],
    'all_code' : ['ALL'],
    'sex_rename' : {'F':'female' , 'M':'male'}
    }
