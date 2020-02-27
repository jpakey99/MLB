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

    #Regular Season games
    for games in schedule:
        if games['home_id'] != 160:
            game = lSim.LaplaceSim(games, standings)
            standings = game.run_simulation()

    #End of regular season, get the final results for the playoffs
    standings.create_divisions()
    standings.playoff_seeding()
    standings.print_standings()
    #Begin the Playoffs with wildcard team
    games = {'game_date': '00-00-00'}
    #NL wildcard game
    games['home_id'] = standings.nl_seeding[3][0]
    games['away_id'] = standings.nl_seeding[4][0]
    game = lSim.LaplaceSim(games, standings)
    standings = game.run_simulation()
    if game.losing_team == standings.nl_seeding[3][0]:
        del standings.nl_seeding[3]
    else:
        del standings.nl_seeding[4]
    #AL Wildcard Game
    games['home_id'] = standings.al_seeding[3][0]
    games['away_id'] = standings.al_seeding[4][0]
    game = lSim.LaplaceSim(games, standings)
    standings = game.run_simulation()
    if game.losing_team == standings.nl_seeding[3][0]:
        del standings.nl_seeding[3]
    else:
        del standings.nl_seeding[4]





simSeason()

