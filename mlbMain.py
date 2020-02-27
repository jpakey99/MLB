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
        #The higher seed is the home team in all the below scenerios
        if game_num == 0 or game_num == 1 and game_num == 5 and game_num == 6 and (game_num == 4 and total_games == 7):
            games['home_id'] = higher_seed
            games['away_id'] = lower_seed
            game = lSim.LaplaceSim(games, standings)
            standings = game.run_simulation()
        #The higher seed is the away team if the above scenerios are not met
        else:
            games['home_id'] = lower_seed
            games['away_id'] = higher_seed
            game = lSim.LaplaceSim(games, standings)
            standings = game.run_simulation()
        #Add the win to the correct team
        if game.losing_team == higher_seed: lower_seed_wins += 1
        else: higher_seed_wins += 1
        #return the result if the a team has won the seres
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
    if losing_team == standings.nl_seeding[3][0]: del standings.nl_seeding[3]
    else: del standings.nl_seeding[4]
    print("The winner of the NL Wildcard Game: ", standings.teams[standings.nl_seeding[3][0]])
    #AL Wildcard Game
    standings, losing_team = sim_playoff_series(standings.al_seeding[3][0], standings.al_seeding[4][0], 1,1, standings)
    if losing_team == standings.nl_seeding[3][0]: del standings.al_seeding[3]
    else: del standings.al_seeding[4]
    print("The winner of the AL Wildcard Game: ", standings.teams[standings.al_seeding[3][0]])
    #NL Divisional Round - Series 1 (1 (0) seed vs 4 (3) seed)
    standings, losing_team0 = sim_playoff_series(standings.nl_seeding[0][0], standings.nl_seeding[3][0], 3, 5, standings)
    #NL Divisional Round - Series 2 (2 (1) seed vs 3 (2) seed)
    standings, losing_team1 = sim_playoff_series(standings.nl_seeding[1][0], standings.nl_seeding[2][0], 3, 5, standings)
    if losing_team0 == standings.nl_seeding[3][0]: del standings.nl_seeding[3]
    if losing_team1 == standings.nl_seeding[2][0]: del standings.nl_seeding[2]
    if losing_team1 == standings.nl_seeding[1][0]: del standings.nl_seeding[1]
    if losing_team0 == standings.nl_seeding[0][0]: del standings.nl_seeding[0]
    print("The NL Divisional Winner:", standings.teams[standings.nl_seeding[0][0]])
    print("The NL Divisional Winner:", standings.teams[standings.nl_seeding[1][0]])

    #AL Divisional Round - Series 1 (1 (0) seed vs 4 (3) seed)
    standings, losing_team0 = sim_playoff_series(standings.al_seeding[0][0], standings.al_seeding[3][0], 3, 5, standings)
    #Al Divisional Round - Series 2 (2 (1) seed vs 3 (2) seed)
    standings, losing_team1 = sim_playoff_series(standings.al_seeding[1][0], standings.al_seeding[2][0], 3, 5, standings)
    if losing_team0 == standings.al_seeding[3][0]: del standings.al_seeding[3]
    if losing_team1 == standings.al_seeding[2][0]: del standings.al_seeding[2]
    if losing_team1 == standings.al_seeding[1][0]: del standings.al_seeding[1]
    if losing_team0 == standings.al_seeding[0][0]: del standings.al_seeding[0]
    print("The AL Divisional Winner:", standings.teams[standings.al_seeding[0][0]])
    print("The AL Divisional Winner:", standings.teams[standings.al_seeding[1][0]])
    #NL Championship Series
    standings, losing_team = sim_playoff_series(standings.nl_seeding[0][0], standings.nl_seeding[1][0], 3, 5, standings)
    if losing_team == standings.nl_seeding[0][0]:
        del standings.nl_seeding[0]
    else:
        del standings.nl_seeding[1]
    print("The NL Champion: ", standings.teams[standings.nl_seeding[0][0]])
    #AL Championship Series
    standings, losing_team = sim_playoff_series(standings.al_seeding[0][0], standings.al_seeding[1][0], 3, 5, standings)
    if losing_team == standings.al_seeding[0][0]:
        del standings.al_seeding[0]
    else:
        del standings.al_seeding[1]
    print("The AL Champion: ", standings.teams[standings.al_seeding[0][0]])
    #World Series
    wold_series_champion = 0
    standings, losing_team = sim_playoff_series(standings.al_seeding[0][0], standings.nl_seeding[0][0], 4, 7, standings)
    if losing_team == standings.al_seeding[0][0]:
        del standings.al_seeding[0]
        wold_series_champion = standings.nl_seeding[0][0]
    else:
        del standings.nl_seeding[0]
        wold_series_champion = standings.al_seeding[0][0]
    print("The World Series Champion: ", standings.teams[wold_series_champion])




simSeason()

