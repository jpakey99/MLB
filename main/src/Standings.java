import java.util.ArrayList;
import java.util.HashMap;

public class Standings {

    private HashMap<Integer, Team> teams;

    public Standings(HashMap<Integer, Team> teams){
        this.teams = teams;
    }

    private ArrayList<Team> getDivisionalStandinds(Divisions division){
        ArrayList<Team> standings = new ArrayList<Team>(5);
        for(Team team : teams.values()){
            if(team.getDivision() == division){
                standings.add(team);
            }
        }
        TeamComparator comparator = new TeamComparator();
        standings.sort(comparator);

        return standings;
    }

    public Team getDivisionalWinner(Divisions division){
        ArrayList<Team> standings = getDivisionalStandinds(division);
        return standings.get(0);
    }

    public ArrayList<Team> getWildCardTeams(){
        ArrayList<Team> wildCards = new ArrayList<Team>(4);
        ArrayList<Team> leagueStandings = new ArrayList<Team>(6);
        ArrayList<Team> tempStandings = new ArrayList<Team>(5);
        TeamComparator comparator = new TeamComparator();

        tempStandings = getDivisionalStandinds(Divisions.ALEAST);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));

        tempStandings = getDivisionalStandinds(Divisions.ALCENTRAL);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));

        tempStandings = getDivisionalStandinds(Divisions.ALWEST);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));
        leagueStandings.sort(comparator);
        wildCards.add(0, leagueStandings.get(0));
        wildCards.add(1, leagueStandings.get(1));

        tempStandings = getDivisionalStandinds(Divisions.NLEAST);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));

        tempStandings = getDivisionalStandinds(Divisions.NLCENTRAL);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));

        tempStandings = getDivisionalStandinds(Divisions.NLWEST);
        leagueStandings.add(tempStandings.get(1));
        leagueStandings.add(tempStandings.get(2));
        leagueStandings.sort(comparator);
        wildCards.add(0, leagueStandings.get(0));
        wildCards.add(1, leagueStandings.get(1));

        return wildCards;
    }

    public void printDivisionalStandings(){
        System.out.println("\t\tAL EAST");
        ArrayList<Team> standings = getDivisionalStandinds(Divisions.ALEAST);

        for (Team team : standings) {
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tAL CENTRAL");
        standings = getDivisionalStandinds(Divisions.ALCENTRAL);

        for (Team team : standings) {
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tAL WEST");
        standings = getDivisionalStandinds(Divisions.ALWEST);

        for (Team team : standings) {
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tNL EAST");
        standings = getDivisionalStandinds(Divisions.NLEAST);

        for (Team team : standings) {
            System.out.println(team + "\t" + team.getWins());
        }

        System.out.println("\t\tNL CENTRAL");
        standings = getDivisionalStandinds(Divisions.NLCENTRAL);

        for (Team team : standings) {
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tNL WEST");
        standings = getDivisionalStandinds(Divisions.NLWEST);

        for (Team team : standings) {
            System.out.println(team + "\t" + team.getWins());
        }
    }
}
