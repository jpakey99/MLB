"""
Author: John Akey <jpakey99@gmail.com>

This class will manage the stnadings of the league.
Main function currently:
    add win total after game
    display standings by win total at the end of the season 
Future Improvements:
    add ability to show league standings
    add ability to show wildcard standings
    make the print out more readable. (Team abbriviations, records, gameback)
    Be able to grab the teams that made the playoffs
"""
class Standings:
    teams = {108:'LAA', 109:'ARI', 110:'BAL', 110:'BAL', 111:'BAL', 112:'CHI', 113:'CIN', 114:'CLE', 115:'COL', 116:'DET', 117:'HOU', 118:'KC', 119:'LAD', 120:'WSH', 121:'NYM', 133:'OAK', 134:'PIT', 135:'SD', 136:'SEA', 137:'SF', 138:'STL', 139:'TB', 140:'TEX', 141:'TOR', 142:'MIN', 143:'PHI', 144:'ATL', 145:'CWS', 146:'MIA', 147:'NYY', 158:'MIL'}
    
    def __init__(self):
        self.records = {}
    
    """
    increments the win total of the team that is passed in.
    winningTeam: team ID, not any other team identifier
    """
    def add_win(self, winningTeam):
        if winningTeam in self.records:
            self.records[winningTeam] += 1
        else:
            self.records[winningTeam] = 1

    """
    A helper function to get the divisional records for an individual division
    In the future, make this more general to deal with wildcard standings as well
    """
    def get_division_standings(self, team1, team2, team3, team4, team5):
        division = {team1:self.records[team1], team2:self.records[team2], team3:self.records[team3], team4:self.records[team4], team5:self.records[team5]}
        return division
    
    """
    creates a sorted list that represents each division.
    """
    def create_divisions(self):
        #AL EAST (110 BAL, 111 BOS, 139 TB, 141 TOR, 147 NYY
        al_east = self.get_division_standings(110, 111, 139, 141, 147)
        self.al_east = sorted(al_east.items(), key=lambda x: x[1], reverse=True)
        #AL CENTRAL (114 CLE, 116 DET, 118 KC, 142 MIN, 145 CWS)
        al_cent = self.get_division_standings(114, 116, 118, 142, 145)
        self.al_cent = sorted(al_cent.items(), key=lambda x: x[1], reverse=True)
        #AL WEST (108 LAA, 117 HOU, 133 OAK, 136 SEA, 140 TEX)
        al_west = self.get_division_standings(108, 117, 133, 136, 140)
        self.al_west = sorted(al_west.items(), key=lambda x: x[1], reverse=True)
        #NL EAST (120 WSH, 121 NYM, 143 PHI, 144 ATL, 146 MIA)
        nl_east = self.get_division_standings(120, 121, 143, 144, 146)
        self.nl_east = sorted(nl_east.items(), key=lambda x: x[1], reverse=True)
        #NL CENTRAL (112 CHC, 113 CIN, 134 PIT, 138 STL, 158 MIL)
        nl_cent = self.get_division_standings(112, 113, 134, 138, 158)
        self.nl_cent = sorted(nl_cent.items(), key=lambda x: x[1], reverse=True)
        #NL WEST (109 ARI, 115 COL, 119 LAD, 135 SD, 137 SF)
        nl_west = self.get_division_standings(109, 115, 119, 135, 137)
        self.nl_west = sorted(nl_west.items(), key=lambda x: x[1], reverse=True)

    """
    helper function that is currently not used.  Strong case for deletion soon
    """
    def sort_divsional_standings(self, division):
        sorted_division = sorted(division.items(), key=lambda x: x[1], reverse=True)
        return sorted_division

    """
    prints the divisional standings.  could use this method to print the other type of standings as well
    """
    def print_standings(self, league=False, wildcard=False, division=True):
        #TODO make team abbriviations be printed instead of team IDs
        if division == True:
            print("AL EAST")
            for tid, win in self.al_east:
                print(self.teams[tid], "\t", win)
            print("AL CENTRAL")
            for tid, win in self.al_cent:
                print(self.teams[tid], "\t", win)
            print("AL WEST")
            for tid, win in self.al_west:
                print(self.teams[tid], "\t", win)
            print("NL EAST")
            for tid, win in self.nl_east:
                print(self.teams[tid], "\t", win)
            print("NL CENTRAL")
            for tid, win in self.nl_cent:
                print(self.teams[tid], "\t", win)
            print("NL WEST")
            for tid, win in self.nl_west:
                print(self.teams[tid], "\t", win)
