import statsapi

schedule = statsapi.schedule(start_date='03/26/2019', end_date='09/20/2019')

for game in schedule:
    box = statsapi.boxscore(game['game_id'])
    print(box)


#game_id, game_date, game_type, status, away_id, home_id, away_score, home_score, winning_team