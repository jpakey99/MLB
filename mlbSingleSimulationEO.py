from random import seed
from random import random

class SingleGameSimulationEO:

    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam

    def runSimulation(self):
        if random() < .5:
            self.winningTeam = self.awayTeam
            self.losingTeam = self.homeTeam
        else:
            self.winningTeam = self.homeTeam
            self.losingTeam = self.awayTeam
