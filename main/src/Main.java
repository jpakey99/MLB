public class Main {
    public static void main(String[] args) {
        Team team1 = new Team(1, null);
        Team team2 = new Team(2, null);
        Player[] playerlist = new Player[9];

        for(int i = 0; i < 9; i++){
            Player player = new Player(i, team1.getTeamId());
            playerlist[i] = player;
        }
        BattingOrder battingOrder1 = new BattingOrder(playerlist);
        team1.setBattingOrder(battingOrder1);

        for(int i = 0; i < 9; i++){
            Player player = new Player(i, team2.getTeamId());
            playerlist[i] = player;
        }
        BattingOrder battingOrder2 = new BattingOrder(playerlist);
        team2.setBattingOrder(battingOrder2);

        Game game = new Game(team1, team2);
        game.simGame();
        System.out.println(game.getWinningTeam());
    }
}
