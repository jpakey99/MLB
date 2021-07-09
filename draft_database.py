import mysql.connector

'''
Team: teamID: int, city_name: str, nickname: str
DraftPick: pickID, round, year, pick_num_round, pick_overall, selection_team, player_first_name, player_last_name, WAR, position, games_played, bonus, type
'''

# connecting to a database
db = mysql.connector.connect(
    host="localhost",
    user="jpakey99",
    database="Baseball" # only include if you want to connect to specific database, must all ready be created
)

# always have this
mycurser = db.cursor(buffered=True)

# creating a table
# datetime: date, ENUM(VALUES): values, NOT NULL: makes sure values are filled
# mycurser.execute("CREATE TABLE DraftPick (pickID INT PRIMARY KEY AUTO_INCREMENT, round INT, year INT,"
#                  "pick_num_round INT, pick_overall INT, selection_team INT, player_first_name VARCHAR(50), player_last_name VARCHAR(50), position VARCHAR(50), WAR FLOAT, games_played INT, bonus INT, type VARCHAR(50),"
#                  "FOREIGN KEY (selection_team) REFERENCES Team(teamID))")
# mycurser.execute("DESCRIBE DraftPick")
# for x in mycurser:
#     print(x)


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
        return y


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
    mycurser.execute("SELECT teamID FROM Team")
    ids = []
    for x in mycurser:
        id = int(x[0])
        ids.append(id)
    return ids


def add_team(id, name, nickname):
    mycurser.execute("INSERT INTO Team (teamID, city_name, nickname) VALUES (%s, %s, %s)", (id, name, nickname))
    db.commit()


# add_basepaths('0')
# print(get_xr_basepath('0'))
# update_basepath_runs('0', 2)

# add elements
# mycurser.execute("INSERT INTO Person (name, age) VALUES (%s, %s)", ("Tim", 19))
# db.commit()

# add_team(1, 'test', 'hey')

# retrieve items
# * = all items, SELECT * FROM ____ WHERE: selects values, ORDER BY
# mycurser.execute("SELECT * FROM DraftPick")
# for x in mycurser:
#     print(x)

# add a column to table
# DROP removes column, CHANGE prev_name new_name TYPE: changes col name
# mycurser.execute("ALTER TABLE Team CHANGE teamID INT PRIMARY KEY")
# db.commit()

# mycurser.execute("DELETE FROM Team where teamID = 1")
# db.commit()
# mycurser.execute("ALTER/ TABLE Games ADD year INT")
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
