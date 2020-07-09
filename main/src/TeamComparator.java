import java.util.Comparator;

public class TeamComparator implements Comparator {
    @Override
    public int compare(Object o1, Object o2) {
        Team team = null;
        Team team1 = null;
        if(o1 instanceof Team){
            team = (Team)o1;
        }
        if(o2 instanceof Team){
            team1 = (Team)o2;
        }
        if(team.getWins() < team1.getWins()){
            return 1;
        }
        else if(team.getWins() == team1.getWins()){
            return 0;
        }
        else{
            return -1;
        }
    }
}
