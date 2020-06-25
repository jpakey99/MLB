import java.util.Random;

public class AtBat {
    private Player batter;
    private AtBatResult result;

    public AtBat(Player batter){
        this.batter = batter;
        this.result = AtBatResult.NONE;
    }

    public Player getBatter() {
        return batter;
    }

    public AtBatResult getResult() {
        return result;
    }

    public void simAtBat(){
        Random rand = new Random();
        float random = rand.nextFloat();

        if(random >= .3527){
            result = AtBatResult.OUT;
        }
        else if(random < .0513){
            result = AtBatResult.DOUBLE;
        }
        else if(.0515 <= random && random < .0565){
            result = AtBatResult.TRIPLE;
        }
        else if(.0565 <= random && random < .0844){
            result = AtBatResult.HOMERUN;
        }
        else if(.0844 <= random && random < .1798){
            result = AtBatResult.WALK;
        }
        else{
            result = AtBatResult.SINGLE;
        }

    }
}
