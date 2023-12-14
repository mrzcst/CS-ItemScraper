import requests
import pandas as pd

url = "https://api.skinport.com/v1/items"
qs = {"app_id":"730","currency":"CNY"}

results = requests.request("GET", url, params=qs)
data = results.json()

if results.status_code != 200:
    print("Error return code: ", results.status_code)

skinPortData = pd.json_normalize(data)
skinPortData.to_json('data/skinport_raw.json')
skinPortData.to_excel('data/skinport_excel.xlsx')

