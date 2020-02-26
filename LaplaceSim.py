from random import seed
from random import random
import statsapi
import Standings


class LaplaceSim:
    """LaplaceSim will run a single game simulation using Laplace's Rule
    Laplace's Rule: (total # of success + 1)/(total # of attempts + 2)"""

    def __init__(self, game, standings):
        self.game = game
        self.home_team = game['home_id']
        self.away_team = game['away_id']
        self.standings = standings

    def run_simulation(self):
        """Runs the single game simulation.
        - at first, just run 50/50 odds until each team has played
        - grab the wins and total games of a team and compute the Laplace number
        - Run the simulation"""
        laplace = .5

        date = self.game['game_date'].split('-')
        if date[1] == '03' or date[1] == '04':
            if random() < .5:
                self.standings.add_win(self.away_team, self.home_team)
            else:
                self.standings.add_win(self.home_team, self.away_team)
        else:
            home_info = self.standings.get_info(self.home_team)
            away_info = self.standings.get_info(self.away_team)
            home_wins = home_info[0] + 1
            home_games = home_info[1] + 2
            away_wins = away_info[0] + 1
            away_games = away_info[1] + 2
            home_laplace = home_wins / home_games
            away_laplace = away_wins / away_games

            if home_laplace > away_laplace:
                laplace = laplace - (home_laplace - away_laplace)
            else:
                laplace = laplace + (away_laplace - home_laplace)

            if random() < laplace:
                self.standings.add_win(self.away_team, self.home_team)
            else:
                self.standings.add_win(self.home_team, self.away_team)
        return self.standings
