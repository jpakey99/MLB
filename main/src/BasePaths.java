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

    public Player getFirstBase(){
        return firstBase;
    }

    public void setFirstBase(Player firstBase) {
        this.firstBase = firstBase;
    }

    public Player getSecondBase() {
        return secondBase;
    }

    public void setSecondBase(Player secondBase) {
        this.secondBase = secondBase;
    }

    public Player getThirdBase() {
        return thirdBase;
    }

    public void setThirdBase(Player thirdBase) {
        this.thirdBase = thirdBase;
    }
}
