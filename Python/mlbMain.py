from dataclasses import dataclass

import statsapi

def get_schedule():
    """Returns the schedule for the entire MLB over a specific range
    The 2020 MLB season goes from '03/26/2020' to '09/28/2020'"""
    startdate = '03/26/2020'
    enddate = '09/28/2020'
    return statsapi.schedule(start_date=startdate, end_date=enddate)


def games_to_csv(games):
    f = open("games.csv", 'w')
    heading = "'gameId', 'gameDate', 'awayId', 'awayName', 'homeId', 'homeName'\n"
    f.write(heading)
    for game in games.values():
        id = str(game['game_id'])
        date = game['game_date']
        away_id = str(game['away_id'])
        away_name = game['away_name']
        home_id = str(game['home_id'])
        home_name = game['home_name']
        buffer = id + ',' + date + ',' + away_id + ',' + away_name + ',' + home_id + ',' + home_name + "\n"
        f.write(buffer)

    f.flush()
    f.close()


def create_dict(games, id):
    games[id] = {
        'game_id': 1,
        'game_date': '',
        'away_id' : 0,
        'away_name': '',
        'home_id': 0,
        'home_name': ''
    }


def add_to_dict(games, game_id, game_date, away_name, home_name, away_id, home_id):
    create_dict(games, game_id)
    games[game_id]['game_id'] = game_id
    games[game_id]['game_date'] = game_date
    games[game_id]['away_name'] = away_name
    games[game_id]['home_name'] = home_name
    games[game_id]['home_id'] = home_id
    games[game_id]['away_id'] = away_id



def get_csv_schedule():
    schedule = get_schedule()

    games = {}

    for game in schedule:
        id = game['game_id']
        add_to_dict(games, id, game['game_date'], game['away_name'], game['home_name'], game['away_id'], game['home_id'] )


    games_to_csv(games)


def main():
    get_csv_schedule()


main()