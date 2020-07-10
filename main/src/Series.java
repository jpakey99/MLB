public class Series {
    private Team higherSeed;
    private Team lowerSeed;
    private int length;
    private Team winningTeam;
    private PlayoffRound round;

    public Series(Team higherSeed, Team lowerSeed, int length, PlayoffRound round){
        this.higherSeed = higherSeed;
        this.lowerSeed = lowerSeed;
        this.length = length;
        this.round = round;
        this.winningTeam = null;
    }

    public Team getWinningTeam() {
        return winningTeam;
    }

    public PlayoffRound getRound(){
        return round;
    }

    public void simSeries(){
        int higherTeamWins = 0;
        int lowerTeamWins = 0;
        for(int i = 0; i < length; i++){
            Game game = new Game(higherSeed, lowerSeed, i);
            game.simGame();
            Team winningTeam = game.getWinningTeam();
            if(winningTeam.equals(higherSeed)){
                higherTeamWins++;
            }
            else{
                lowerTeamWins++;
            }
            if(higherTeamWins > length/2){
                winningTeam = higherSeed;
                return;
            }else if(lowerTeamWins > length/2){
                winningTeam = lowerSeed;
                return;
            }
        }
    }


}
