import requests
import csv
import pandas as pd
pd.set_option('display.max_columns', None) # Displays all columns when viewing the DF
import time
import numpy as np

# Contains stats of points per game in the NBA 2012-13
test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2012-13&SeasonType=Regular%20Season&StatCategory=PTS'

# GET request to retrieve test_url
request_api = requests.get(url=test_url).json()
table_headers = request_api['resultSet']['headers']

# Preparing the DF
df_cols = ['Year', 'Season_type'] + table_headers
df = pd.DataFrame(columns=df_cols)

# Here we want to specify the seasons from the data we want to scrape from
season_types = ['Regular%20Season', 'Playoffs']
years = ['2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

# To avoid blocking from the NBA API to prove we are not a bot
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com',
    'Sec-Ch-Ua': 'Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}
# Start time for loop
begin_loop = time.time()

for y in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
        request_api = requests.get(url=api_url, headers=headers).json()
        temp_df1 = pd.DataFrame(request_api['resultSet']['rowSet'], columns=table_headers)
        temp_df2 = pd.DataFrame({'Year': [y for i in range(len(temp_df1))],
                         'Season_type': [s for i in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
        df = pd.concat([df, temp_df3], axis=0)
        print(f'Finished scraping data for the {y} {s}')
        lag = np.random.uniform(low=5, high=40)
        print(f'...waiting {round(lag, 1)} seconds')
        time.sleep(lag)

print(f'Process completed. Total run time: {round((time.time()-begin_loop)/60, 2)}')
df.to_csv('nba_player_data.csv', index=False)
