public class Walk implements AtBatResult {
    private Player player;

    public Walk(Player player){
        this.player = player;
    }

    @Override
    public int handleResult(BasePaths basePaths) {
        int score = 0;

        if(basePaths.getThirdBase() != null && basePaths.getSecondBase() != null && basePaths.getFirstBase() != null){
            score++;
            basePaths.setThirdBase(basePaths.getSecondBase());
            basePaths.setSecondBase(basePaths.getFirstBase());
        }
        if(basePaths.getSecondBase() != null && basePaths.getFirstBase() != null){
            basePaths.setThirdBase(basePaths.getSecondBase());
            basePaths.setSecondBase(basePaths.getFirstBase());
        }
        if(basePaths.getFirstBase() != null){
            basePaths.setSecondBase(basePaths.getFirstBase());
        }
        basePaths.setFirstBase(player);

        return score;
    }
}
