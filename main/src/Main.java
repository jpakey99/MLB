import java.util.HashMap;

public class Main {
    public static void main(String[] args) {

        //Create all 30 Teams manually
        HashMap<Integer, Team> teams = new HashMap<>();
        //AL EAST
        teams.put(147, new Team(147, null, "New York Yankees", Divisions.ALEAST));
        teams.put(110, new Team(110, null, "Baltimore Orioles", Divisions.ALEAST));
        teams.put(111, new Team(111, null, "Boston Red Sox  ", Divisions.ALEAST));
        teams.put(141, new Team(141, null, "Toronto Blue Jays", Divisions.ALEAST));
        teams.put(139, new Team(139, null, "Tampa Bay Rays  ", Divisions.ALEAST));
        //AL CENTRAL
        teams.put(118, new Team(118, null, "Kansas City Royals", Divisions.ALCENTRAL));
        teams.put(145, new Team(145, null, "Chicago White Sox", Divisions.ALCENTRAL));
        teams.put(116, new Team(116, null, "Detroit Tigers  ", Divisions.ALCENTRAL));
        teams.put(114, new Team(114, null, "Cleveland Indians", Divisions.ALCENTRAL));
        teams.put(142, new Team(142, null, "Minnesota Twins  ", Divisions.ALCENTRAL));
        //AL WEST
        teams.put(140, new Team(140, null, "Texas Rangers    ", Divisions.ALWEST));
        teams.put(136, new Team(136, null, "Seattle Mariners", Divisions.ALWEST));
        teams.put(108, new Team(108, null, "Los Angeles Angels", Divisions.ALWEST));
        teams.put(117, new Team(117, null, "Houston Astros  ", Divisions.ALWEST));
        teams.put(133, new Team(133, null, "Oakland Athletics", Divisions.ALWEST));
        //NL EAST
        teams.put(120, new Team(120, null, "Washington Nationals", Divisions.NLEAST));
        teams.put(121, new Team(121, null, "New York Mets       ", Divisions.NLEAST));
        teams.put(143, new Team(143, null, "Philadelphia Phillies", Divisions.NLEAST));
        teams.put(146, new Team(146, null, "Miami Marlins       ", Divisions.NLEAST));
        teams.put(144, new Team(144, null, "Atlanta Braves      ", Divisions.NLEAST));
        //NL CENTRAL
        teams.put(134, new Team(134, null, "Pittsburgh Pirates", Divisions.NLCENTRAL));
        teams.put(112, new Team(112, null, "Chicago Cubs    ", Divisions.NLCENTRAL));
        teams.put(158, new Team(158, null, "Milwaukee Brewers", Divisions.NLCENTRAL));
        teams.put(113, new Team(113, null, "Cincinnati Reds  ", Divisions.NLCENTRAL));
        teams.put(138, new Team(138, null, "St. Louis Cardinals", Divisions.NLCENTRAL));
        //NL WEST
        teams.put(137, new Team(137, null, "San Francisco Giants", Divisions.NLWEST));
        teams.put(119, new Team(119, null, "Los Angeles Dodgers  ", Divisions.NLWEST));
        teams.put(115, new Team(115, null, "Colorado Rockies    ", Divisions.NLWEST));
        teams.put(135, new Team(135, null, "San Diego Padres    ", Divisions.NLWEST));
        teams.put(109, new Team(109, null, "Arizona Diamondbacks", Divisions.NLWEST));

        csvFileReader fileReader = new csvFileReader();
        Schedule schedule = fileReader.readSchedule(teams);

        Player[] playerlist = new Player[9];

        for(Team team : teams.values()) {
            for (int i = 0; i < 9; i++) {
                Player player = new Player(i, team.getTeamId());
                playerlist[i] = player;
            }
            BattingOrder battingOrder1 = new BattingOrder(playerlist);
            team.setBattingOrder(battingOrder1);
        }

        Standings standings = new Standings(teams);

        Season season = new Season(schedule, standings);
        season.simEntireSeason();

        standings.printDivisionalStandings();
    }
}
