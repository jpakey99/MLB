import mlbSingleSimulationEO as mlbSSEO
import statsapi

# game = mlbSSEO.SingleGameSimulationEO("Pirates", "Reds")
# game.runSimulation()
# print(game.winningTeam)

pirates = 0
records = {}

def record(winningTeam):
    global records

    if winningTeam in records:
        records[winningTeam] += 1
    else:
        records[winningTeam] = 1

def calcWinner(game):
    global pirates
    if game.winningTeam == 134:
        pirates = pirates + 1
    record(game.winningTeam)

def standings():
    global records
    #AL EAST (110 BAL, 111 BOS, 139 TB, 141 TOR, 147 NYY)
    al_east = {110:records[110], 111:records[111], 139:records[139], 141:records[141], 147:records[147]}
    al_east_sorted = sorted(al_east.items(), key=lambda x: x[1], reverse=True)
    #AL CENTRAL (114 CLE, 116 DET, 118 KC, 142 MIN, 145 CWS)
    al_cent = {114:records[114], 116:records[116], 118:records[118], 142:records[142], 145:records[145]}
    al_cent_sorted = sorted(al_cent.items(), key=lambda x: x[1], reverse=True)
    #AL WEST (108 LAA, 117 HOU, 133 OAK, 136 SEA, 140, TEX)
    al_west = {108:records[108], 117:records[117], 133:records[133], 136:records[136], 140:records[140]}
    al_west_sorted = sorted(al_west.items(), key=lambda x: x[1], reverse=True)
    #NL EAST (120 WSH, 121 NYM, 143 PHI, 144 ATL, 146 MIA)
    nl_east = {120:records[120], 121:records[121], 143:records[143], 144:records[144], 146:records[146]}
    nl_east_sorted = sorted(nl_east.items(), key=lambda x: x[1], reverse=True)
    #NL CENTRAL (112 CHC, 113 CIN, 134 PIT, 138 STL, 158 MIL)
    nl_cent = {112:records[112], 113:records[113], 134:records[134], 138:records[138], 158:records[158]}
    nl_cent_sorted = sorted(nl_cent.items(), key=lambda x: x[1], reverse=True)
    #NL WEST (109 ARI, 115 COL, 119 LAD, 135 SD, 137 SF)
    nl_west = {109:records[109], 115:records[115], 119:records[119], 135:records[135], 137:records[137]}
    nl_west_sorted = sorted(nl_west.items(), key=lambda x: x[1], reverse=True)
    #PRINT (change into helper function latter
    print("AL EAST", al_east_sorted)
    print("AL CENT", al_cent_sorted)
    print("AL WEST", al_west_sorted)
    print("NL EAST", nl_east_sorted)
    print("NL CENT", nl_cent_sorted)
    print("NL WEST", nl_west_sorted)

def simSeason():
    schedule = statsapi.schedule(start_date='03/26/2020', end_date='09/28/2020')

    for games in schedule:
        game = mlbSSEO.SingleGameSimulationEO(games['home_id'], games['away_id'])
        game.runSimulation()
        calcWinner(game)
    standings()

simSeason()
