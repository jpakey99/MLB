import java.util.ArrayList;

public class Season {
    private Schedule schedule;
    private Standings standings;

    public Season(Schedule schedule, Standings standings){
        this.schedule = schedule;
        this.standings = standings;
    }

    private void simRegularSeason(){
        for(int i = 0; i < schedule.getLengthOfSchedule(); i++){
            Game game = schedule.getNextGame();
            game.simGame();
            game.getWinningTeam().updateWins();
        }
    }

    private Team simWildcard(ArrayList<Team> wildCard){

    }

    public void simEntireSeason(){
        simRegularSeason();
        ArrayList<Team> alStandings = standings.getPlayoffSeeding("AL");
        ArrayList<Team> nlStandings = standings.getPlayoffSeeding("NL");
        ArrayList<Team> wildcard = (ArrayList<Team>) alStandings.subList(4, 5);
        Team winner = simWildcard(wildcard);

    }

}
