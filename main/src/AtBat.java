import java.util.Random;

public class AtBat {
    private Player batter;
    private AtBatResult result;

    public AtBat(Player batter){
        this.batter = batter;
        this.result = null;
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
            result = new Out();
        }
        else if(random < .0513){
            result = new Double(batter);
        }
        else if(.0515 <= random && random < .0565){
            result = new Triple(batter);
        }
        else if(.0565 <= random && random < .0844){
            result = new HomeRun(batter);
        }
        else if(.0844 <= random && random < .1798){
            result = new Walk(batter);
        }
        else{
            result = new Single(batter);
        }
    }
}
