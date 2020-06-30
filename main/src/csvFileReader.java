import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

public class csvFileReader  {
     public HashSet<Game> readSchedule(HashMap<Integer, Team> teams){
         File file = new File("C:\\Users\\jpake\\Documents\\MLB\\games.csv");
         HashSet<Game> schedule = new HashSet<>();
         try {
             Scanner scanner = new Scanner(file);
             scanner.nextLine();
             while(scanner.hasNextLine()){
                String data = scanner.nextLine();
                String[] split = data.split(",");
                int gameId = Integer.parseInt(split[0]);
                int awayId = Integer.parseInt(split[2]);
                Team awayTeam = teams.get(awayId);
                int homeId = Integer.parseInt(split[4]);
                Team homeTeam = teams.get(homeId);
                Game game = new Game(homeTeam, awayTeam, gameId);
                schedule.add(game);
             }
         } catch (FileNotFoundException e) {
             e.printStackTrace();
         }
         return schedule;
     }
}
