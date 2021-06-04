import pybaseball
from team_stats import TeamStats


class TeamPitchingStats(TeamStats):
    def __init__(self, year: int):
        super().__init__(pybaseball.team_pitching(year))

    def xfip_adjusted(self):
        return self.get_data('xFIP-')

    def pace(self):
        return self.get_data('Pace')

    def strikeouts_nine_adjusted(self):
        return self.get_data('K/9+')

    def walks_nine_adjusted(self):
        return self.get_data('BB/9+ ')

    def hit_nine_adjusted(self):
        return self.get_data('H/9+')

    def homerun_nine_adjusted(self):
        return self.get_data('HR/9+')

    def average_adjusted(self):
        return self.get_data('AVG+')

    def babip_adjusted(self):
        return self.get_data('BABIP+')

    def soft_adjusted(self):
        return self.get_data('Soft%+')

    def hard_adjusted(self):
        return self.get_data('Hard%+')

    def runs(self):
        return self.get_data('R')