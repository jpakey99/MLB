import mlbSingleSimulationEO as mlbSSEO
import LaplaceSim as lSim
import Standings
import statsapi

def get_schedule(startdate, enddate):
    """Returns the schedule for the entire MLB over a specific range
    The 2020 MLB season goes from '03/26/2020' to '09/28/2020'"""
    return statsapi.schedule(start_date=startdate, end_date=enddate)

def simSeason():
    schedule = get_schedule('03/26/2020', '09/28/2020')
    standings = Standings.Standings()

    for games in schedule:
        if games['home_id'] != 160:
            game = lSim.LaplaceSim(games, standings)
            standings = game.run_simulation()
    standings.create_divisions()
    standings.print_standings()

simSeason()

