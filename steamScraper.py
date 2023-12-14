import requests
import pandas as pd

url = "https://steamcommunity.com/market/search/render"

pages = 0
while(pages < 10):
    querystring = {"start":"0","count":"100","sort_column":"name","appid":"730","norender":"1"}
    response = requests.request("GET", url, params=querystring)
    pages = int(response.json()["total_count"]/100 + 1)

results = []
for page in range(1, pages):
    start = 100 * (page - 1)
    print('Scraping page', page, 'out of', pages)
    
    querystring = {"start":f"{start}","count":"100","sort_column":"name","appid":"730","norender":"1"}
    try:
        response = requests.request("GET", url, params=querystring)
        items = response.json()["results"]
    except KeyError:
        print("Error while scraping Steam! Retry later!")
        break

    for item in items:
        results.append(item)

steamData = pd.json_normalize(results)
steamData.to_json('data/steam_raw.json')
steamData.to_excel('data/steam_excel.xlsx')
