import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashSet;
import java.util.Scanner;

public class csvFileReader  {
     public void readSchedule(HashSet<Team> teams){
         File file = new File("C:\\Users\\jpake\\Documents\\MLB\\Python\\games.csv");
         try {
             Scanner scanner = new Scanner(file);
             while(scanner.hasNextLine()){
                String data = scanner.nextLine();
                String[] split = data.split(",");
                String awayTeam = split[2];
                String homeTeam = split[3];

             }
         } catch (FileNotFoundException e) {
             e.printStackTrace();
         }

     }
}
