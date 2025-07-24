import pandas as pd
import requests

url = "https://files.digital.nhs.uk/FC/187D35/health_care_ld_sicbl_2023-24.csv"
df_emis = pd.read_csv(url)

response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the content of the response to a local CSV file
    with open("docs/emis_calculation/LD_data.csv", "wb") as f:
        f.write(response.content)

else:
    print("Failed to download CSV file. Status code:", response.status_code)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("LD_data.csv")

# Need to filter the codes LDOB089 and LDOB091
adhd_counts = df_emis