import java.util.Comparator;

public class Team {
    private int teamId;
    private int wins;
    private String teamName;
    private BattingOrder battingOrder;
    private Divisions division;

    public Team(int teamId, BattingOrder battingOrder, String teamName, Divisions division){
        this.teamId = teamId;
        this.battingOrder = battingOrder;
        this.teamName = teamName;
        this.division = division;
        this.wins = 0;
    }

    public int getWins(){
        return wins;
    }

    public void updateWins(){
        this.wins += 1;
    }

    public String getTeamName(){
        return this.teamName;
    }

    public int getTeamId() {
        return teamId;
    }

    public void setBattingOrder(BattingOrder battingOrder){
        this.battingOrder = battingOrder;
    }

    public BattingOrder getBattingOrder() {
        return battingOrder;
    }

    public Divisions getDivision(){
        return division;
    }

    @Override
    public String toString() {
        return teamName;
    }

    public boolean equals(Object o){
        if(o instanceof Team){
            Team team = (Team)o;
            return team.teamId == this.teamId;
        }
        return false;
    }
}
