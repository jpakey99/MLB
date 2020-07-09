import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.TreeMap;

public class Standings {

    private HashMap<Integer, Team> teams;

    public Standings(HashMap<Integer, Team> teams){
        this.teams = teams;
    }

    private ArrayList<Team> getDivisionalStandinds(Divisions division){
        ArrayList<Team> standings = new ArrayList(5);
        for(Team team : teams.values()){
            if(team.getDivision() == division){
                standings.add(team);
            }
        }
        TeamComparator comparator = new TeamComparator();
        standings.sort(comparator);

        return standings;
    }

    public void printDivisionalStandings(){
        System.out.println("\t\tAL EAST");
        ArrayList<Team> standings = getDivisionalStandinds(Divisions.ALEAST);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tAL CENTRAL");
        standings = getDivisionalStandinds(Divisions.ALCENTRAL);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tAL WEST");
        standings = getDivisionalStandinds(Divisions.ALWEST);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tNL EAST");
        standings = getDivisionalStandinds(Divisions.NLEAST);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t" + team.getWins());
        }

        System.out.println("\t\tNL CENTRAL");
        standings = getDivisionalStandinds(Divisions.NLCENTRAL);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t\t" + team.getWins());
        }

        System.out.println("\t\tNL WEST");
        standings = getDivisionalStandinds(Divisions.NLWEST);

        for(int i = 0; i < standings.size(); i++){
            Team team = standings.get(i);
            System.out.println(team + "\t" + team.getWins());
        }
    }
}
