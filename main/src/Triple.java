public class Triple implements AtBatResult {
    private Player player;

    public Triple(Player player){
        this.player = player;
    }

    @Override
    public int handleResult(BasePaths basePaths) {
        int score = 0;

        if(basePaths.getThirdBase() != null){
            score++;
            basePaths.setThirdBase(null);
        }
        if(basePaths.getSecondBase() != null){
            score++;
            basePaths.setSecondBase(null);
        }
        if(basePaths.getFirstBase() != null){
            score++;
            basePaths.setFirstBase(null);
        }
        basePaths.setThirdBase(player);

        return score;
    }
}
