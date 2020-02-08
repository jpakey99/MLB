import mlbSingleSimulationEO as mlbSSEO
import statsapi

# game = mlbSSEO.SingleGameSimulationEO("Pirates", "Reds")
# game.runSimulation()
# print(game.winningTeam)

pirates = 0

def calcWinner(game):
    global pirates
    if game.winningTeam == 134:
        pirates = pirates + 1


def simSeason():
    schedule = statsapi.schedule(start_date='03/26/2020', end_date='09/28/2020')

    for games in schedule:
        game = mlbSSEO.SingleGameSimulationEO(games['home_id'], games['away_id'])
        game.runSimulation()
        calcWinner(game)

simSeason()
print(pirates)
