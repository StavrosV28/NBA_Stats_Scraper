import scrape_Stats
import pandas as pd

def main():
    data = pd.read_csv('nba_player_data.csv')
    
    data.drop(columns=['RANK', 'EFF'], inplace=True)
    
    data['season_start_year'] = data['Year'].str[:4].astype(int)
    
    data.replace(to_replace=['NOP', 'NOH'], value='NO')
    
    data['Season_type'].replace('Regular%20Season', 'Regular Season')
    
    reg_sn = data[data['Season_type'] == 'Regular Season']
    playoffs = data[data['Season_type'] == 'Regular Season']
    
    print(data.columns)
    
    total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']
    
    data_per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum().reset_index()
    
    
    for col in data_per_min[4:]:
        data_per_min[col] = data_per_min[col] / data_per_min['MIN']    
    
    data_per_min['FG%'] = data_per_min['FGM']/data_per_min['FGA']
    data_per_min['3PT%'] = data_per_min['FG3M']/data_per_min['FG3A']
    data_per_min['FT%'] = data_per_min['FTM']/data_per_min['FTA']
    data_per_min['FG3A%'] = data_per_min['FG3A']/data_per_min['FGA']
    data_per_min['PTS/FGA'] = data_per_min['PTS']/data_per_min['FGA']
    data_per_min['FG3M/FGM'] = data_per_min['FG3M']/data_per_min['FGM']
    data_per_min['FTA/FGA'] = data_per_min['FTA']/data_per_min['FGA']
    data_per_min['TRU%'] = 0.5*data_per_min['PTS']/(data_per_min['FGA']+0.475*data_per_min['FTA'])
    data_per_min['AST_TOV'] = data_per_min['AST']/data_per_min['TOV']
    
    print(data_per_min)
    
    
   
    
    
if __name__ == '__main__':
    main()
    
    


