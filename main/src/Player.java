public class Player {
    private int playerId;
    private int teamId;

    public Player(int playerId, int teamId){
        this.playerId = playerId;
        this.teamId = teamId;
    }

    public void setTeamId(int teamId){
        this.teamId = teamId;
    }

    public int getPlayerId(){
        return this.playerId;
    }

    public int getTeamId(){
        return this.teamId;
    }

    @Override
    public String toString() {
        return "Player{" +
                "player Id: " + playerId +
                ", plays for team: " + teamId +
                '}';
    }
}
