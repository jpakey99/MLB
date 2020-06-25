public class BattingOrder {
    private int index;
    private Player[] battingOrder;

    public BattingOrder(Player[] battingOrder){
        this.index = 0;
        this.battingOrder = battingOrder;
    }

    public void incrementOrder(){
        if(index > 7){
            this.index = 0;
        }
        this.index++;
    }

    public Player getBatter(){
        Player player = battingOrder[index];
        incrementOrder();
        return player;
    }

    public void setBattingOrder(Player[] battingOrder){
        this.battingOrder = battingOrder;
    }
}
