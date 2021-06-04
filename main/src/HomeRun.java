public class HomeRun implements AtBatResult {
    private Player player;

    public HomeRun(Player player){
        this.player = player;
    }

    @Override
    public int handleResult(BasePaths basePaths) {
        int score = 0;
        score++;
        if(basePaths.getThirdBase() != null){
            score++;
        }
        if(basePaths.getSecondBase() != null){
            score++;
        }
        if(basePaths.getThirdBase() != null){
            score++;
        }
        basePaths.clearBasePaths();
        return score;
    }
}
