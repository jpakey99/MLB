public class Game implements GameInterface{
    private Team homeTeam;
    private Team awayTeam;
    private boolean completed;
    private int homeScore;
    private int awayScore;
    private Team winningTeam;
    private int gameId;

    public Game(Team homeTeam, Team awayTeam, int gameId){
        this.homeTeam = homeTeam;
        this.awayTeam = awayTeam;
        this.completed = false;
        this.awayScore = 0;
        this.homeScore = 0;
        this.winningTeam = null;
        this.gameId = gameId;
    }

    public int getGameId() {
        return gameId;
    }

    public Team getHomeTeam() {
        return homeTeam;
    }

    public Team getAwayTeam() {
        return awayTeam;
    }

    public boolean isCompleted() {
        return completed;
    }

    public int getHomeScore() {
        return homeScore;
    }

    public int getAwayScore() {
        return awayScore;
    }

    public Team getWinningTeam() {
        return winningTeam;
    }

    private void setWinningTeam(){
        if(homeScore > awayScore){
            winningTeam = homeTeam;
        }
        else{
            winningTeam = awayTeam;
        }
    }

    private boolean isGameOver(int inning, int homeScore, int awayScore, boolean topOfInning){
        if(inning >= 9 && !topOfInning && homeScore > awayScore){
            return true;
        }
        else return inning >= 10 && topOfInning && homeScore != awayScore;
    }

    public void simGame(){
        int outs;
        int runs;
        int inning = 1;
        boolean topOfInning = true;
        BattingOrder currentBattingOrder;
        BasePaths basePaths = new BasePaths();

        while(!isGameOver(inning, homeScore, awayScore, topOfInning)){
            outs = 0;
            runs = 0;
            if(topOfInning){
                currentBattingOrder = awayTeam.getBattingOrder();
            }
            else{
                currentBattingOrder = homeTeam.getBattingOrder();
            }
            while(outs < 3){
                Player batter = currentBattingOrder.getBatter();
                AtBat atBat = new AtBat(batter);
                atBat.simAtBat();
                AtBatResult result = atBat.getResult();

                if(result instanceof Out){
                    outs++;
                }
                else{
                    runs += result.handleResult(basePaths);
                }
            }
            if(topOfInning){
                awayScore = runs;
                topOfInning = false;
            }
            else{
                homeScore = runs;
                topOfInning = true;
                inning++;
            }
            basePaths.clearBasePaths();
        }
        completed = true;
        setWinningTeam();
    }

    @Override
    public String toString() {
        if(this.completed){
            return this.gameId + " " + awayTeam + ":" + awayScore + " @ " + homeTeam + ":" + homeScore;
        }
        else{
            return this.gameId + " " + awayTeam + " @ " + homeTeam;
        }
    }
}
