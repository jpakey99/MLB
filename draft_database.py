import mysql.connector

'''
Team: teamID: int, city_name: str, nickname: str
DraftPick: pickID, round, year, pick_num_round, pick_overall, selection_team, player_first_name, player_last_name, WAR, position, games_played, bonus, type
DraftPool: selection_team, pool, picks
'''

user_input = input("Please enter database password")

# connecting to a database
db = mysql.connector.connect(
    host="localhost",
    user="jpakey99",
    passwd=user_input,
    database="Baseball" # only include if you want to connect to specific database, must all ready be created
)

# always have this
mycurser = db.cursor(buffered=True)

# creating a table
# datetime: date, ENUM(VALUES): values, NOT NULL: makes sure values are filled
# mycurser.execute("CREATE TABLE DraftPool (selection_team INT, pool INTEGER, picks INTEGER,"
#                  "FOREIGN KEY (selection_team) REFERENCES Team(teamID))")
# mycurser.execute("DESCRIBE DraftPick")
# for x in mycurser:
#     print(x)


def add_pool(team, pool, picks, year):
    mycurser.execute("INSERT INTO DraftPool (selection_team, pool, picks, year)"
                     " VALUES (%s, %s, %s, %s)", (team, pool, picks, year))
    db.commit()


def get_player_drafted_year(year):
    sql = "SELECT player_first_name, player_last_name, selection_team FROM DraftPick WHERE year = %s"
    mycurser.execute(sql, (year,))
    picks = []
    for x in mycurser:
        picks.append((x[0], x[1], x[2]))
    return picks


def get_pool_per_pick(team, year):
    sql = "SELECT pool, picks FROM DraftPool WHERE selection_team = %s AND year = %s"
    mycurser.execute(sql, (team, year))
    for x in mycurser:
        string = str(x[0]/x[1])
        k = string.split('.')
        keep_index = len(k[0]) - 4
        temp_string = k[0]
        dec = keep_index - 1
        temp = temp_string[0:keep_index]
        final = temp[0:dec] + '.' + temp[dec:]
        print(final, x[0]/x[1])
        return float(final)


def add_draft_pick(round, year, pick_num_round, pick_overall, selection_team, player_first_name, player_last_name, WAR, games_played, bonus, type, position):
    mycurser.execute("INSERT INTO DraftPick (round, year, pick_num_round, pick_overall, selection_team, player_first_name, player_last_name, position, WAR, games_played, bonus, type)"
                     " VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s)", (round, year, pick_num_round, pick_overall, selection_team, player_first_name,
                                                                                player_last_name, position, WAR, games_played, bonus, type))
    db.commit()


def get_teamID_from_nickname(nickname):
    sql = "SELECT teamID FROM Team WHERE nickname = %s"
    mycurser.execute("SELECT teamID FROM Team WHERE nickname = %s", (nickname,))
    for x in mycurser:
        y = x[0]
        return int(y)


def get_draft_pick_war_per_team_year_year(teamId, year):
    sql = "SELECT war, games_played FROM DraftPick WHERE year = %s AND selection_team = %s"
    value = (year, teamId)
    mycurser.execute(sql, value)
    total_war, total_games = 0, 0
    for x in mycurser:
        total_war += x[0]
        total_games += x[1]
    if total_games == 0:
        return 0
    return (total_war/total_games)*162


def get_war_per_162_for_pick(pick):
    sql = "SELECT war, games_played FROM DraftPick WHERE pick_overall = %s"
    value = (pick,)
    mycurser.execute(sql, value)
    total_war = 0
    total_games = 0
    for x in mycurser:
        total_war += x[0]
        total_games += x[1]
    return (total_war/total_games) *162


# print(get_war_per_162_for_pick(20))
# sql = "SELECT games_played FROM DraftPick WHERE selection_team = %s"
# value = (109,)
# mycurser.execute(sql, value)
# players = 0
# for x in mycurser:
#     print(x)
#     if x[0] >= 1:
#         players += 1


def get_total_mlb_players_from_team_draft_year(teamId, year):
    sql = "SELECT games_played FROM DraftPick WHERE year = %s AND selection_team = %s"
    value = (year, teamId)
    mycurser.execute(sql, value)
    players = 0
    for x in mycurser:
        if x[0] >= 1:
            players += 1
    return players


def retrieve_teamids():
    mycurser.execute("SELECT teamID, nickname FROM Team")
    ids = []
    for x in mycurser:
        id = int(x[0])
        ids.append(id)
    return ids


def add_team(id, name, nickname):
    mycurser.execute("INSERT INTO Team (teamID, city_name, nickname) VALUES (%s, %s, %s)", (id, name, nickname))
    db.commit()


# retrieve items
# * = all items, SELECT * FROM ____ WHERE: selects values, ORDER BY
# mycurser.execute("UPDATE Team SET nickname='Diamondbacks' WHERE teamID = 109")
# mycurser.execute("SELECT * FROM DraftPool")
# db.commit()
# for x in mycurser:
#     print(x)

# add a column to table
# DROP removes column, CHANGE prev_name new_name TYPE: changes col name
# mycurser.execute("ALTER TABLE Team CHANGE teamID INT PRIMARY KEY")
# db.commit()

# mycurser.execute("DELETE FROM DraftPool")
# mycurser.execute("ALTER TABLE DraftPool ADD year INT")
# db.commit()
# mycurser.execute("ALTER/ TABLE Games ADD year INT")
# mycurser.execute("ALTER TABLE Games ADD month INT")
# mycurser.execute("ALTER TABLE Games ADD day INT")

# mycurser.execute("DESCRIBE DraftPick")
# for x in mycurser:
#     print(x)
# mycurser.execute("DELETE FROM Basepaths")

# mycurser.execute("SELECT * FROM Basepaths")
# index = 0
# for x in mycurser:
#     print(x)
#     index += 1
# print(index)
