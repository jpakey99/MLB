public class Double implements AtBatResult {
    private Player player;

    public Double(Player player){
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
            basePaths.setThirdBase(basePaths.getFirstBase());
            basePaths.setFirstBase(null);
        }
        basePaths.setSecondBase(player);
        return score;
    }
}
