from random import seed
from random import random
import statsapi
import Standings

class LaplaceSim:
    standings = Standings.Standings()

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.game_num = 0;

    def run_simulation(self):
        #(tot success + 1)/(tot attempts + 2)
        #first simulation if 50/50
        if self.game_num <= 15:
            if random() < .5:
                self.winning_team = self.away_team
                self.losing_team = self.home_team
            else:
                self.winning_team = self.home_team
                self.losing_team = self.away_team
            
            self.game_num = self.game_num + 1
        else:
            home_info = standings.get_info(self.home_team)
            away_info = standings.get_info(self.away_team)
            home_wins = home_info[0] + 1
            home_games = home_info[1] + 2
            away_wins = away_info[0] + 1
            away_games = away_info[1] + 2
            home_laplace = home_wins / home_games
            away_laplace = away_wins / away_games
            laplace = .5

            if home_lapace > away_lapace:
                laplace = laplace - (home_laplace - away_laplace)
            else:
                laplace = laplace + (away_laplace - home_laplace)
            
            if random() < laplace:
                self.winning_team = self.away_team
                self.losing_team = self.home_team
            else:
                self.winning_team = self.home_team
                self.losing_team = self.away_team
