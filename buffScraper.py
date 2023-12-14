# Getting info from Buff Market
import requests
import pandas as pd
import time

""" 
    HOW TO GET THE REQUIRED COOKIES

1. Log in your Buff163 account
2. Inspect the page 
3. Select [Application] from Activity Bar 
4. Select [Cookies] 
5. Copy and Insert the required cookies 

The reason you need this is because you can not scrape all the pages other way, 
Buff163 restricts guests and using your Session ID you will scrape using your account.

USE AT YOUR OWN RISK, IF YOU SCRAPE AT A HIGH SPEED YOU CAN GET BANNED
"""

# Required Cookies (Should be completed)
device_id = "TO BE COMPLETED"
session = "TO BE COMPLETED"
client_id = "TO BE COMPLETED"
csrf_token = "TO BE COMPLETED"

# Page changing cooldown (If <5 can get your account restricted) 
page_cooldown = 5

#=========================================================================================================================================#

url = "https://buff.163.com/api/market/goods"
querystring = {"game":"csgo","page_num":"1","page_size":"80"}
headers = {
    "Cookie": f"Device-Id={device_id}; Locale-Supported=en; game=csgo; session={session}; client_id={client_id}; csrf_token={csrf_token}"
}

get_pages = requests.request("GET", url, headers=headers, params=querystring)
pages = int(get_pages.json()['data']['total_count']/80) + 1

results = []
for page in range(1, pages):
    print('Scraping page', page, 'out of', pages)

    querystring = {"game":"csgo","page_num":f"{page}","page_size":"80"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    
    try:
        data = response.json()
        for item in data['data']['items']:
            results.append(item)
        time.sleep(page_cooldown)
    except KeyError:
        print(f"Error at page {page}! Try correct cookies!")
        break

buffData = pd.json_normalize(results)
buffData.to_json('data/buff_raw.json')
buffData.to_excel('data/buff_excel.xlsx')