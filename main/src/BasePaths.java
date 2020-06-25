public class BasePaths {
    private Player firstBase;
    private Player secondBase;
    private Player thirdBase;

    public BasePaths(){
        firstBase = null;
        secondBase = null;
        thirdBase = null;
    }

    public void clearBasePaths(){
        firstBase = null;
        secondBase = null;
        thirdBase = null;
    }

    public int handleEvent(Player player, AtBatResult result){
        int score = 0;
        if(result == AtBatResult.SINGLE){
            if(thirdBase != null){
                score++;
                thirdBase = null;
            }
            if(secondBase != null){
                thirdBase = secondBase;
                secondBase = null;
            }
            if(firstBase != null){
                secondBase = firstBase;
                firstBase = null;
            }
            firstBase = player;
        }
        else if(result == AtBatResult.DOUBLE){
            if(thirdBase != null){
                score++;
                thirdBase = null;
            }
            if(secondBase != null){
                score++;
                secondBase = null;
            }
            if(firstBase != null){
                thirdBase = firstBase;
                firstBase = null;
            }
            secondBase = player;
        }
        else if(result == AtBatResult.TRIPLE){
            if(thirdBase != null){
                score++;
                thirdBase = null;
            }
            if(secondBase != null){
                score++;
                secondBase = null;
            }
            if(firstBase != null){
                score++;
                firstBase = null;
            }
            thirdBase = player;
        }
        else if(result == AtBatResult.HOMERUN){
            score++;
            if(thirdBase != null){
                score++;
            }
            if(secondBase != null){
                score++;
            }
            if(firstBase != null){
                score++;
            }
            clearBasePaths();
        }
        else{
            if(thirdBase != null && secondBase != null && firstBase != null){
                score++;
                thirdBase = secondBase;
                secondBase = firstBase;
            }
            if(secondBase != null && firstBase != null){
                thirdBase = secondBase;
                secondBase = firstBase;
            }
            if(firstBase != null){
                secondBase = firstBase;
            }
            firstBase = player;
        }
        return score;
    }
}
