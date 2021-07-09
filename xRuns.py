import pybaseball, mlbgame, statsapi, requests, datetime
import database


xR = {
        '0000': 0.033, '0001': 0.026, '0002': 0.019,
        '1000': 0.132, '1001': 0.116, '1002': 0.155,
        '1100': 0.204, '1101': 0.276, '1102': 0.441,
        '1110': 1.101, '1111': 1.242, '1112': 1.375,
        '1010': 0.937, '1011': 1.066, '1012': 1.124,
        '0100': 0.249, '0101': 0.265, '0102': 0.681,
        '0110': 1.159, '0111': 1.176, '0112': 1.350,
        '0010': 0.974, '0011': 0.932, '0012': 0.970
}

situations = {
        '0000': [0]*6, '0001': [0]*6, '0002': [0]*6,
        '1000': [0]*6, '1001': [0]*6, '1002': [0]*6,
        '1100': [0]*6, '1101': [0]*6, '1102': [0]*6,
        '1110': [0]*6, '1111': [0]*6, '1112': [0]*6,
        '1010': [0]*6, '1011': [0]*6, '1012': [0]*6,
        '0100': [0]*6, '0101': [0]*6, '0102': [0]*6,
        '0110': [0]*6, '0111': [0]*6, '0112': [0]*6,
        '0010': [0]*6, '0011': [0]*6, '0012': [0]*6
}


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


class Play:
    def __init__(self, play, bases=None):
        pass


class BaseRunningPlay(Play):
    pass


class BattingPlay(Play):
    def __init__(self, play, rbi, outs, bases=None):
        super().__init__(play)
        # self.outs = play['count']['outs']
        self.rbi = rbi
        self.outs = outs
        self.play = play
        self.inning = play['about']['inning']
        if bases is None:
            self.bases = BasePaths(0)
            self.end_state = self.get_end_state_bases()
        else:
            self.bases = bases
            self.end_state = self.get_end_state_bases()
        self.xruns = xR[self.bases.convert_to_xrun_string()]

    def get_end_state_bases(self):
        self.end_outs = self.play['count']['outs']
        end_state = BasePaths(outs=self.outs, b1=False, b2=False, b3=False)
        for runner in self.play['runners']:
            # print(len(self.play['runners']), runner)
            if runner['movement']['start'] == '1B':
                end_state.first = True
            if runner['movement']['start'] == '2B':
                end_state.second = True
            if runner['movement']['start'] == '3B':
                end_state.third = True
        return end_state

class Team:
    def __init__(self, id, name):
        self.id, self.name = id, name
        self.xR = 0.0

    def add_xR(self, xR):
        self.xR += xR


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.boxscore = statsapi.get('game', {'gamePk': game_id})
        self.home_team = Team(self.boxscore['gameData']['teams']['home']['id'], self.boxscore['gameData']['teams']['home']['name'])
        self.away_team = Team(self.boxscore['gameData']['teams']['away']['id'], self.boxscore['gameData']['teams']['away']['name'])
        self.box_plays = self.boxscore['liveData']['plays']['allPlays']
        self.clean_plays = []
        self.plays = []
        self.half_inning_starts = self.get_half_inning_starts()

    def get_half_inning_starts(self):
        inning_start = []
        for play in self.boxscore['liveData']['plays']['playsByInning']:
            # print(play)
            if len(play['bottom']) > 0:
                inning_start.append((play['top'][0], play['bottom'][0]))
            else:
                inning_start.append((play['top'][0], -1))
        return inning_start

    def is_start_inning(self, atBat_index):
        for inning in self.half_inning_starts:
            if atBat_index in inning:
                return True
        return False

    def get_clean_plays(self):
        # prev_play = None
        outs = 0
        for play in self.box_plays:
            # print(play['result']['rbi'])
            if self.is_start_inning(play['atBatIndex']):
                c_bases = BattingPlay(play, play['result']['rbi'],0)
                self.clean_plays.append(c_bases)
                outs = c_bases.end_outs
                # prev_play = c_bases.end_state
            else:
                c_bases = BattingPlay(play,play['result']['rbi'], outs)
                self.clean_plays.append(c_bases)
                outs = c_bases.end_outs
                # prev_play = c_bases.end_state
            if c_bases.end_state.convert_to_xrun_string() == '0003':
                print(play)
            database.update_basepath_runs(c_bases.end_state.convert_to_xrun_string(), play['result']['rbi'])
            situations[c_bases.end_state.convert_to_xrun_string()][play['result']['rbi']] += 1
            situations[c_bases.end_state.convert_to_xrun_string()][-1] += 1
            self.plays.append((c_bases.bases.convert_to_xrun_string(), play['result']['rbi']))


    def allocate_xR(self):
        for play in self.clean_plays:
            if play.play['about']['halfInning'] == 'top':
                self.away_team.add_xR(play.xruns)
            elif play.play['about']['halfInning'] == 'bottom':
                self.home_team.add_xR(play.xruns)
        # print(self.home_team.name, self.home_team.xR, self.away_team.name, self.away_team.xR)


if __name__ == '__main__':
    # teams = statsapi.get('teams', {'activeStatus': 'Y'})
    # for team in teams['teams']:
    #     if 'id' in team['league']:
    #         if team['league']['id'] == 103 or team['league']['id'] == 104:
    #             city_name, team_name, id = team['locationName'], team['teamName'], team['id']
    #             print(team['locationName'], team['teamName'], team['id'])
    #             database.add_team(id, city_name, team_name)

    # games = statsapi.schedule(date=datetime.datetime.now().date())
    games = statsapi.schedule(date='2021-06-14')

    # print(statsapi.meta('leagueIds'))
    # games = statsapi.schedule(start_date='2021-04-01', end_date='2021-06-12')
    # print(statsapi.meta('gameTypes'))

    # Individual Game Test
    # g = Game(games[0]['game_id'])
    # # game_date, winning_team
    # if games[0]['away_name'] == games[0]['winning_team']:
    #     print(games[0]['away_id'])
    # if games[0]['home_name'] == games[0]['winning_team']:
    #     print(games[0]['home_id'])
    # for thing in games[0]:
    #     print(thing)
    # print(games[0]['game_date'].split('-'))
    # print(games[0]['status'])
    # g.get_clean_plays()
    # g.allocate_xR()

    plays = []
    ids = database.retrieve_game_id()
    teams = database.retrieve_teamids()
    print(teams)
    num_plays = len(games)
    num = num_plays
    c, gn = 0, 0
    # print(situations['0000'][0])
    for game in games:
        ids = database.retrieve_game_id()
        if (game['game_type'] != 'S' or game['game_type'] != 'N' or game['game_type'] != 'A' or game['game_type'] != 'I' or game['game_type'] != 'E'):
            g = Game(game['game_id'])
            g.get_clean_plays()
            g.allocate_xR()
            plays.append(g.plays)
            ascore, hscore, axr, hxr = int(game['away_score']), int(game['home_score']), g.away_team.xR, g.home_team.xR
            run_share, xrun_share = hscore - ascore, hxr - axr
            if run_share != 0 and xrun_share != 0:
                if (run_share < 0 and xrun_share < 0) or (run_share > 0 and xrun_share > 0):
                    correct = True
                    c += 1
                else:
                    correct = False
                gn += 1
                year, month, day = game['game_date'].split('-')
                winner = 0
                if 'winning_team' in game:
                    if game['away_name'] == game['winning_team']:
                        winner = game['away_id']
                    if game['home_name'] == game['winning_team']:
                        winner = game['home_id']
                    away_team, home_team = g.away_team.id, g.home_team.id
                    if away_team in teams and home_team in teams:
                        # print(game['game_id'], num, year, month, day, away_team, home_team)
                        # database.add_game(game['game_id'], away_team, home_team, ascore, hscore, axr, hxr, winner, year, month, day)
                        print(g.away_team.name, g.away_team.xR, g.home_team.name, g.home_team.xR, run_share, xrun_share, correct)
                    else: print(away_team, home_team)
                # print(away_team, home_team, winner, year, month, day, game['game_id'])
        num -= 1
    print(c/gn)


