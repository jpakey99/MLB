import java.util.ArrayList;

public class Schedule {
    private ArrayList<Game> games;
    private int index;

    public Schedule(ArrayList<Game> games){
        this.games = games;
        this.index = 0;
    }

    public ArrayList<Game> getGames() {
        return games;
    }

    public int getLengthOfSchedule(){
        return games.size();
    }

    public Game getNextGame(){
        if(index < games.size()) {
            Game game = this.games.get(index);
            index++;
            return game;
        }
        else{
            return null;
        }
    }

    @Override
    public String toString() {
        String result  = "";
        for(Game game : games){
            result = result + game.getGameId() + ",";
        }
        return result;
    }
}
