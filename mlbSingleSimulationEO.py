"""
Author: John Akey <jpakey99@gmail.com>
"""
from random import seed
from random import random

"""
The class will simulate one game with 50/50 odds for each team to win the game.
homeTeam/awayTeam can either be team ids or team names
"""
class SingleGameSimulationEO:

    #initalizes the object
    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
    
    #runs the simulation.  away team wins if random returns a number less than .5
    def runSimulation(self):
        if random() < .5:
            self.winningTeam = self.awayTeam
            self.losingTeam = self.homeTeam
        else:
            self.winningTeam = self.homeTeam
            self.losingTeam = self.awayTeam
