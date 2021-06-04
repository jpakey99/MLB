import pybaseball, mlbgame, statsapi, requests, datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

startdate = '02/28/2020'
enddate = '04/01/2020'


def get_run_expectancy(situation):
    re = {
        '0000': 0.461, '0001': 0.243, '0002': 0.095,
        '1000': 0.831, '1001': 0.489, '1002': 0.214,
        '1100': 1.373, '1101': 0.908, '1102': 0.343,
        '1110': 2.282, '1111': 1.520, '1112': 0.736,
        '1010': 1.798, '1011': 1.140, '1012': 0.471,
        '0100': 1.068, '0101': 0.644, '0102': 0.305,
        '0110': 1.920, '0111': 1.352, '0112': 0.570,
        '0010': 2.282, '0011': 1.520, '0012': 0.736
    }
    return re[situation]



def graph(x, y):
    fig = plt.figure(figsize=(23, 10.4))
    ax = fig.add_subplot()
    plt.margins(0.01, 0.01)
    axis = plt.gca()
    axis.set_ylim(0, 100)
    y_index, y_s_index, x_index, x_s_index = [], [], [], []
    for num in range(0, 110, 10):
        y_index.append(num)
        y_s_index.append(str(num))
    for num in y:
        x_index.append(num)
        x_s_index.append(str(num))
    plt.yticks(y_index, y_s_index)
    plt.xticks(x_index, x_s_index)
    plt.grid()
    plt.plot(y, x)
    plt.show()


def win_prob(games):
    # game_winProbability
    game = games[0]['game_id']
    wp = statsapi.get('game_winProbability', {'gamePk': game})
    # print(wp)
    wp_play = []
    for play in wp:
        wp_play.append(play['homeTeamWinProbability'])
    index = list(range(0, len(wp_play)))
    # print(index, wp_play)
    # print(wp_play)
    graph(wp_play, index)
    # print(wp)



def live_game():
    # print(datetime.datetime.now().date())
    # pbp = statsapi.schedule(date=datetime.datetime.now().date())
    pbp = statsapi.schedule(date='2021-06-03')
    return pbp


# print(play['about']['halfInning'], play['about']['inning'], '\touts' ,play['count']['outs'], '\t runnerIndex', play['runnerIndex'])
class BasePaths:
    def __init__(self, outs, b1=False, b2=False, b3=False):
        self.first, self.second, self.third = b1, b2, b3
        self.outs = outs

    def __str__(self):
        return '1: ' + str(self.first) + ' 2: ' + str(self.second) + ' 3: ' + str(self.third) + ' OUTS: ' + str(self.outs)

    def convert_to_xrun_string(self):
        buffer = ''
        if self.first:
            buffer += '1'
        else:
            buffer += '0'
        if self.second:
            buffer += '1'
        else:
            buffer += '0'
        if self.third:
            buffer += '1'
        else:
            buffer += '0'
        buffer += str(self.outs)
        return buffer


def get_start_innings(boxscore):
    inning_start = []
    for play in boxscore['liveData']['plays']['playsByInning']:
        # print(play)
        if len(play['bottom']) > 0:
            inning_start.append((play['top'][0], play['bottom'][0]))
        else:
            inning_start.append((play['top'][0], -1))
    return inning_start


def is_start_inning(inning_start, at_bat_index):
    for inning in inning_start:
        if at_bat_index in inning:
            return True
    return False


def get_runners_at_end_of_atbat(play):
    outs = play['count']['outs']
    print(outs)
    previous_base = BasePaths(outs=outs, b1=False, b2=False, b3=False)
    for runner in play['runners']:
        if runner['movement']['end'] == '1B':
            previous_base.first = True
        if runner['movement']['end'] == '2B':
            previous_base.second = True
        if runner['movement']['end'] == '3B':
            previous_base.third = True
    return previous_base


def xruns(game):
    # print(game)
    boxscore = statsapi.get('game', {'gamePk': game['game_id']})
    # boxscore = statsapi.boxscore_data(game['game_id'])
    inning_start = get_start_innings(boxscore)
    # print(inning_start)
    previous_base = None
    for play in boxscore['liveData']['plays']['allPlays']:
        current_at_bat = play['atBatIndex']
        new_inning = is_start_inning(inning_start, current_at_bat)
        runners = []
        if new_inning:
            bases = BasePaths(0)
            previous_base = get_runners_at_end_of_atbat(play)
            runners.append(bases)
        else:
            runners.append(previous_base)
            previous_base = get_runners_at_end_of_atbat(play)

        # for play in runners:
        #     print(play.convert_to_xrun_string())
            # print(get_run_expectancy(play.convert_to_xrun_string()))


games = live_game()
# win_prob(games)
xruns(games[4])

# # for e in ge:
# #     hi = e.bottom
# #     for at in hi:
# #         for key in at.__dict__.keys():
# #             print(key)
# # print(statsapi.schedule(start_date=startdate, end_date=enddate, team=134))
# # print(statsapi.boxscore_data(605799))
# # print(requests.get('http://statsapi.mlb.com//api/v1/game/565803/linescore.json'))
# pbp = statsapi.get('game', {'gamePk':605799})
# for key in pbp:
#     print(key)
# print()
# # print(pbp['gameData'])
# for play in pbp['liveData']['plays']['allPlays']:
#     # for key in pbp['liveData']['plays']['allPlays']:
#     #     print(key)
#     print(play['runners'])
#     # print(play['batter'])


def draft():
    pdick = {}


    # ad = pybaseball.amateur_draft(2009, 1, keep_stats=False)
    # print(ad['Name'], ad['Type'])
    # players = ad['Name']
    # p = players[0].split(' ')
    # last, first = p[1].strip('\\xa0').lower(), p[0].lower()
    # l, f = last.strip(), first.strip()
    # print(l, f)
    # pid = pybaseball.playerid_lookup(last=l, first=f, fuzzy=True)
    # for i in pid:
    #     if i == 'key_bbref':
    #         pass
    s = pybaseball.bwar_bat()
    for line in s:
        print(line)
    p, y,w, t  = s['player_ID'], s['year_ID'], s['WAR'], s['team_ID']
    l = []
    print(len(p))
    for i in range(0, len(p)):
        # print(int(y[1]) == 2006, int(y[1]))
        if y[i] == 2021:
            l.append((p[i], y[i], w[i], t[i]))
            print(p[i], y[i], w[i], t[i])
    # print(len(l))
    # print(pid)
    # pdick[l+f] = {
    #     'key_bbref' : pid['key_bbref'],
    #     'key_fangraphs': pid['key_fangraphs'],
    #     'key_retro': pid['key_retro']
    # }
    #
    # for player in pdick:
    #     for key in pdick[player]:
    #         print(pdick[player][key])
