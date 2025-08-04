import pandas as pd
import requests
from config import config
import os
import zipfile

def create_source_files_from_nhs_england(config):
    """
    Downloads files from URLs specified in the config dictionary, saves them to a specified directory,
    and extracts any ZIP files found in that directory.

    Args:
        config (dict): A configuration dictionary containing:
            - Keys with 'url' in their name, each mapping to a file URL to download.
            - 'file_path_to_save' (str): Directory path where files will be saved and extracted.

    Raises:
        KeyError: If 'file_path_to_save' is not present in the config.
        requests.exceptions.RequestException: If a download request fails.
        zipfile.BadZipFile: If a ZIP file is corrupted or invalid.

    Side Effects:
        - Downloads files from the specified URLs and saves them to disk.
        - Extracts all ZIP files in the target directory.
    """

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