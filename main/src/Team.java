public class Team {
    private int teamId;
    private String teamName;
    private BattingOrder battingOrder;

    public Team(int teamId, BattingOrder battingOrder, String teamName){
        this.teamId = teamId;
        this.battingOrder = battingOrder;
        this.teamName = teamName;
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

    @Override
    public String toString() {
        return teamName + " : " + teamId;
    }
}
