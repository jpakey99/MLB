public class Team {
    private int teamId;
    private BattingOrder battingOrder;

    public Team(int teamId, BattingOrder battingOrder){
        this.teamId = teamId;
        this.battingOrder = battingOrder;
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
        return "Team{" +
                "team Id: " + teamId +
                '}';
    }
}
