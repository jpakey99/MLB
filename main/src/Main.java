import java.util.HashMap;

public class Main {
    public static void main(String[] args) {

        //Create all 30 Teams manually
        HashMap<Integer, Team> teams = new HashMap<>();
        //AL EAST
        teams.put(147, new Team(147, null, "New York Yankees"));
        teams.put(110, new Team(110, null, "Baltimore Orioles"));
        teams.put(111, new Team(111, null, "Boston Red Sox"));
        teams.put(141, new Team(141, null, "Toronto Blue Jays"));
        teams.put(139, new Team(139, null, "Tampa Bay Rays"));
        //AL CENTRAL
        teams.put(118, new Team(118, null, "Kansas City Royals"));
        teams.put(145, new Team(145, null, "Chicago White Sox"));
        teams.put(116, new Team(116, null, "Detroit Tigers"));
        teams.put(114, new Team(114, null, "Cleveland Indians"));
        teams.put(142, new Team(142, null, "Minnesota Twins"));
        //AL WEST
        teams.put(140, new Team(140, null, "Texas Rangers"));
        teams.put(136, new Team(136, null, "Seattle Mariners"));
        teams.put(108, new Team(108, null, "Los Angeles Angels"));
        teams.put(117, new Team(117, null, "Houston Astros"));
        teams.put(133, new Team(133, null, "Oakland Athletics"));
        //NL EAST
        teams.put(120, new Team(120, null, "Washington Nationals"));
        teams.put(121, new Team(121, null, "New York Mets"));
        teams.put(143, new Team(143, null, "Philadelphia Phillies"));
        teams.put(146, new Team(146, null, "Miami Marlins"));
        teams.put(144, new Team(144, null, "Atlanta Braves"));
        //NL CENTRAL
        teams.put(134, new Team(134, null, "Pittsburgh Pirates"));
        teams.put(112, new Team(112, null, "Chicago Cubs"));
        teams.put(158, new Team(158, null, "Milwaukee Brewers"));
        teams.put(113, new Team(113, null, "Cincinnati Reds"));
        teams.put(138, new Team(138, null, "St. Louis Cardinals"));
        //NL WEST
        teams.put(137, new Team(137, null, "San Francisco Giants"));
        teams.put(119, new Team(119, null, "Los Angeles Dodgers"));
        teams.put(115, new Team(115, null, "Colorado Rockies"));
        teams.put(135, new Team(135, null, "San Diego Padres"));
        teams.put(109, new Team(109, null, "Arizona Diamondbacks"));

        csvFileReader fileReader = new csvFileReader();
        fileReader.readSchedule(teams);
//        Player[] playerlist = new Player[9];
//
//        for(int i = 0; i < 9; i++){
//            Player player = new Player(i, team1.getTeamId());
//            playerlist[i] = player;
//        }
//        BattingOrder battingOrder1 = new BattingOrder(playerlist);
//        team1.setBattingOrder(battingOrder1);
//
//        for(int i = 0; i < 9; i++){
//            Player player = new Player(i, team2.getTeamId());
//            playerlist[i] = player;
//        }
//        BattingOrder battingOrder2 = new BattingOrder(playerlist);
//        team2.setBattingOrder(battingOrder2);
//
//        Game game = new Game(team1, team2);
//        game.simGame();
//        System.out.println(game.getWinningTeam());
    }
}
