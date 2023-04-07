
# Setup
import pandas as pd
import requests

API_KEY = "oBp3SutzgAnKqfSubeTauNHHMSJw9KniFaNcqLHA"

# Choose start and end dates
START_DATE = '2009-01'
END_DATE = '2023-01'

URL = "https://api.eia.gov/v2/crude-oil-imports/data/"

PARAMS = {
    'api_key':API_KEY,
    'frequency':'monthly',
    'start':START_DATE,
    'end':END_DATE,
    'data[0]':'quantity',
    'length':'5000',
    'offset':'0',
    'sort[0][column]':'period',
    'sort[0][direction]':'desc'
}

final_data = []
status = True
offset = 0

print("Importing data...")
while status:

    PARAMS['offset'] = str(offset)
    
    r = requests.get(url=URL, params=PARAMS, timeout=300)
    json_data = r.json()

    if r.status_code == 200:
        raw_data = json_data['response']['data']
        if len(raw_data) == 5000:
            df = pd.DataFrame(raw_data)
        else:
            status = False
    else:
        raise ConnectionError(f"Data pull request failed with code: {r.status_code}")

    offset += 5000      
    final_data.append(df)

final_df = pd.concat(final_data, ignore_index=True)
final_df.rename(columns={'period':'date'}, inplace=True)
print("Completed!")

# Export data
filename = "Crude_Oil_Imports.xlsx"
final_df.to_excel(filename, index=False)
