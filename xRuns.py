import pybaseball, mlbgame, statsapi, requests, datetime


xR = {
        '0000': 0.461, '0001': 0.243, '0002': 0.095,
        '1000': 0.831, '1001': 0.489, '1002': 0.214,
        '1100': 1.373, '1101': 0.908, '1102': 0.343,
        '1110': 2.282, '1111': 1.520, '1112': 0.736,
        '1010': 1.798, '1011': 1.140, '1012': 0.471,
        '0100': 1.068, '0101': 0.644, '0102': 0.305,
        '0110': 1.920, '0111': 1.352, '0112': 0.570,
        '0010': 2.282, '0011': 1.520, '0012': 0.736
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
    def __init__(self, play, bases=None):
        super().__init__(play)
        # self.outs = play['count']['outs']
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
        outs = self.play['count']['outs']
        end_state = BasePaths(outs=outs, b1=False, b2=False, b3=False)
        for runner in self.play['runners']:
            if runner['movement']['end'] == '1B':
                end_state.first = True
            if runner['movement']['end'] == '2B':
                end_state.second = True
            if runner['movement']['end'] == '3B':
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
        self.home_team = None
        self.away_team = None
        self.boxscore = statsapi.get('game', {'gamePk': game_id})
        self.box_plays = self.boxscore['liveData']['plays']['allPlays']
        self.clean_plays = []
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
        # update to loop over plays per inning, with that, add xR to the correct team
        prev_play = None
        for play in self.box_plays:
            if self.is_start_inning(play['atBatIndex']):
                c_bases = BattingPlay(play)
                self.clean_plays.append(c_bases)
                prev_play = c_bases.end_state
            else:
                c_bases = BattingPlay(play, prev_play)
                self.clean_plays.append(c_bases)
                prev_play = c_bases.end_state


if __name__ == '__main__':
    # print(datetime.datetime.now().date())
    # games = statsapi.schedule(date=datetime.datetime.now().date())
    games = statsapi.schedule(date='2021-06-03')
    game = Game(games[4]['game_id'])
    game.get_clean_plays()

