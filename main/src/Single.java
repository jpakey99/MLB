public class Single implements AtBatResult {
    private Player player;

    public Single(Player player){
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
            basePaths.setThirdBase(basePaths.getSecondBase());
            basePaths.setSecondBase(null);
        }
        if(basePaths.getFirstBase() != null){
            basePaths.setSecondBase(basePaths.getFirstBase());
            basePaths.setFirstBase(null);
        }
        basePaths.setFirstBase(player);
        return score;
    }
}
