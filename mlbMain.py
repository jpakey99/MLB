import mlbSingleSimulationEO as mlbSSEO
import Standings
import statsapi

# game = mlbSSEO.SingleGameSimulationEO("Pirates", "Reds")
# game.runSimulation()
# print(game.winningTeam)

def simSeason():
    schedule = statsapi.schedule(start_date='03/26/2020', end_date='09/28/2020')
    standings = Standings.Standings()

    for games in schedule:
        game = mlbSSEO.SingleGameSimulationEO(games['home_id'], games['away_id'])
        game.runSimulation()
        standings.add_win(game.winningTeam)
    standings.create_divisions()
    standings.print_standings()

simSeason()
