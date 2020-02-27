import mlbSingleSimulationEO as mlbSSEO
import LaplaceSim as lSim
import Standings
import statsapi

def get_schedule(startdate, enddate):
    """Returns the schedule for the entire MLB over a specific range
    The 2020 MLB season goes from '03/26/2020' to '09/28/2020'"""
    return statsapi.schedule(start_date=startdate, end_date=enddate)

def sim_regular_season(schedule, standings):
    """Sims a full MLB regular season
    schedule - the full regular season schedule
    standings - the standings aboject to be used throughout the season
    return - standings object"""
    for games in schedule:
        if games['home_id'] != 160:
            game = lSim.LaplaceSim(games, standings)
            standings = game.run_simulation()
    return standings

def sim_playoff_series(higher_seed, lower_seed, first_to, total_games, standings):
    """Sims 1 playoff round
    high_seed - team_id of the higher seeded team (team with the lower index in the seeding list
    lower_seed - team_id of the lower seeded team (team with the higher index in the seeding list
    first_to - how many wins a team needs in order to move on
    total_games - the amount of games played in the series
    standings - the standings object used throughout the season
    return - standings and the team_id that losses the series"""
    higher_seed_wins = 0
    lower_seed_wins = 0
    games = {'game_date': '00-00-00'}
    for game_num in range(0, total_games):
        games['home_id'] = higher_seed
        games['away_id'] = lower_seed
        game = lSim.LaplaceSim(games, standings)
        standings = game.run_simulation()
        if game.losing_team == higher_seed: lower_seed_wins += 1
        else: higher_seed_wins += 1

        if higher_seed_wins == first_to: return standings, lower_seed
        elif lower_seed_wins == first_to: return standings, higher_seed
        else: pass

def simSeason():
    schedule = get_schedule('03/26/2020', '09/28/2020')
    standings = Standings.Standings()

    standings = sim_regular_season(schedule, standings)

    #End of regular season, get the final results for the playoffs
    standings.create_divisions()
    standings.playoff_seeding()
    standings.print_standings()
    #NL wildcard game
    standings, losing_team = sim_playoff_series(standings.nl_seeding[3][0], standings.nl_seeding[4][0], 1,1, standings)
    if losing_team == standings.nl_seeding[3][0]:
        del standings.nl_seeding[3]
    else:
        del standings.nl_seeding[4]
    #AL Wildcard Game
    standings, losing_team = sim_playoff_series(standings.al_seeding[3][0], standings.al_seeding[4][0], 1,1, standings)
    if losing_team == standings.nl_seeding[3][0]:
        del standings.al_seeding[3]
    else:
        del standings.al_seeding[4]
    #NL Divisional Round - Series 1

    #NL Divisional Round - Series 2

    #AL Divisional Round - Series 1

    #Al Divisional Round - Series 2

    #NL Championship Series

    #AL Championship Series

    #World Series





simSeason()

