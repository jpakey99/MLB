import statsapi
import datetime
import mlbgame

def get_schedule():
    """Returns the schedule for the entire MLB over a specific range
    The 2020 MLB season goes from '03/26/2020' to '09/28/2020'"""
    startdate = '02/28/2020'
    enddate = '04/01/2020'
    return statsapi.schedule(start_date=startdate, end_date=enddate, team=134)


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
    test = schedule[11]
    a = statsapi.boxscore_data(test['game_id'])['awayBatters'][1:]
    for batter in a:
        if not batter['substitution']:
            print("{}\t{}\t{}".format(int(batter['battingOrder'])/100, batter['position'], batter['name']))
    games_to_csv(games)


def read_from_csv(file_name):
    pass


def write_to_csv(file_name, r_dict, starting_date: datetime.date, end_date: datetime.date):
    heading = 'date,'
    date = starting_date
    player_keys = []
    file = open(file_name, 'w')
    # for key in dict, add to the heading -> add keys to player_keys
    for key in r_dict.keys():
        heading += str(key) + ','
        player_keys.append(key)
    heading += '\n'
    file.write(heading)
    # pick the starting date for the season -> use the player_keys to see if player was on roster that day
    while date <= end_date:
        buffer = str(date) + ','
        date_string = str(date)
        for player in player_keys:
            # if on roster and if in lineup -> write batting order spot to file
            l = r_dict[player]['on_roster']
            for day in l:
                if day == date_string:
                    bl = r_dict[player]['lineup']
                    for d in bl:
                        if d[0] == date_string:
                            buffer += str(d[1]) + ','
                    buffer += ','
            buffer += '0,'
        buffer += '\n'
        file.write(buffer)
        date = date + datetime.timedelta(days=1)
    file.close()

    # if on roster and not in lineup -> write a comma and move on
    # else -> write a 0
    pass


def create_lineup_dict(dict, player_name):
    dict[player_name] = {
        'on_roster': [],
        'lineup': [],
        'position': {
            'c': 0,
            '1b' : 0,
            '2b': 0,
            '3b': 0,
            'ss': 0,
            'lf': 0,
            'cf': 0,
            'rf': 0,
            'dh': 0
        }
    }


def lineup(box, r_dict, date):
    for batter in box:
        if not batter['substitution']:
            order = int(int(batter['battingOrder']) / 100)
            name = batter['name'].split(',')[0]
            position = batter['position'].lower()
            if name in r_dict.keys():
                r_dict[name]['lineup'].append([date, order])
            else:
                create_lineup_dict(r_dict, name)
                r_dict[name]['lineup'].append([date, order])
            r_dict[name]['position'][position] += 1
    return r_dict


def roster(date, r_dict: dict):
    active = statsapi.roster(134, rosterType='Active', date=date).split('\n')
    for player in active:
        player = player.split()
        if len(player) > 1:
            if player[1] != 'P':
                if player[3] in r_dict.keys():
                    r_dict[player[3]]['on_roster'].append(date)
                else:
                    create_lineup_dict(r_dict, player[3])
                    r_dict[player[3]]['on_roster'].append(date)
    return r_dict


def get_lineup_info():
    schedule = get_schedule()
    r_dict = {}
    days = []
    for game in schedule:
        date = game['game_date']
        if game['away_id'] == 134 and game['status'] != 'Postponed':
            box = statsapi.boxscore_data(game['game_id'])['awayBatters'][1:]
            r_dict = roster(date, r_dict)
            r_dict = lineup(box, r_dict, date)
        elif game['home_id'] == 134 and game['status'] != 'Postponed':
            box = statsapi.boxscore_data(game['game_id'])['homeBatters'][1:]
            r_dict = roster(date, r_dict)
            r_dict = lineup(box, r_dict, date)
    return r_dict


def box_score():
    startdate = '02/28/2021'
    enddate = '10/01/2021'
    now = datetime.datetime.now()
    bs = statsapi.boxscore_data(605799, timecode=now)
    print(bs)
    for key in bs.keys():
        print(key)
        if type(bs[key]) is dict:
            for k in bs[key].keys():
                print('\t', k)
    print(bs['home']['battingOrder'])


def main():
    box_score()
    # s = get_schedule()
    # print(len(s))
    # for game in s:
    #     print(game)
    # r_dict = get_lineup_info()
    # starting_date = datetime.date(2020, 7, 24)
    # print(starting_date)
    # end_date = datetime.date.today()
    # write_to_csv('batting_order.csv', r_dict, starting_date, end_date)


main()