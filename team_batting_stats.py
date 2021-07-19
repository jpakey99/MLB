import pybaseball

import team_stats
from team_stats import TeamStats


class TeamBattingStats(TeamStats):
    def __init__(self, year: int):
        super().__init__(pybaseball.team_batting(year))

    def wrc_adjusted(self):
        return self.get_data('wRC+')

    def obp_adjusted(self):
        return self.get_data('OBP+')

    def xba(self):
        return self.get_data('xBA')

    def average_adjusted(self):
        return self.get_data('AVG+')

    def iso_adjusted(self):
        return self.get_data('ISO+')

    def babip_adjusted(self):
        return self.get_data('BABIP+')

    def slugging_adjusted(self):
        return self.get_data('SLG+')

    def walk_adjusted(self):
        return self.get_data('BB%+')

    def strikeout_adjusted(self):
        return self.get_data('K%+')

    def linedrive_adjusted(self):
        return self.get_data('LD+%')

    def groundball_adjusted(self):
        return self.get_data('GB%+')

    def flyball_adjusted(self):
        return self.get_data('FB%+')

    def homerun_to_flyball_adjusted(self):
        return self.get_data('HR/FB%+')

    def pull_adjusted(self):
        return self.get_data('Pull%+')

    def cent_adjusted(self):
        return self.get_data('Cent%+')

    def oppo_adjusted(self):
        return self.get_data('Oppo%+')

    def soft_adjusted(self):
        return self.get_data('Soft%+')

    def medium_adjusted(self):
        return self.get_data('Med%+')

    def hard_adjusted(self):
        return self.get_data('Hard%+')

    def runs(self):
        return self.get_data('R')

    def xruns(self):
        return self.get_data('RE24')


def organize_data(team, stat):
    team_list, data_list, combined_list = [], [], []
    for t in team:
        team_list.append(t)
    for w in stat:
        data_list.append(w)
    for i in range(0, len(team_list)):
        combined_list.append((team_list[i], data_list[i]))
    return combined_list


if __name__ == '__main__':
    # tb = TeamBattingStats(2021)
    # print(tb.data)
    ts = team_stats.TeamStandings(2021)
    print(ts.get_standings())