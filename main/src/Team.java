public class Team {
    private int teamId;
    private String teamName;
    private BattingOrder battingOrder;
    private Divisions division;

    public Team(int teamId, BattingOrder battingOrder, String teamName, Divisions division){
        this.teamId = teamId;
        this.battingOrder = battingOrder;
        this.teamName = teamName;
        this.division = division;
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
}
