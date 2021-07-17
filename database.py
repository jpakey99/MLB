import mysql.connector

'''
Team: teamID: int, city_name: str, nickname: str
Basepaths: basepaths_id: str, zero_runs: int, one_runs: int, two_runs: int, three_runs: int, four_runs: int
Games: gameID: int, away_team: teamID, home_team: teamID, away_score: int, home_score: int, away_xR: float, home_xR: float, winner: teamID
DraftPick: pickID, Round, Year, pick_num_round, pick_overall, selection_team, player_first_name, player_last_name, WAR, position, games_played, bonus, type
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

# How to create a database
# mycurser.execute("CREATE DATABASE Baseball")

# creating a table
# datetime: date, ENUM(VALUES): values, NOT NULL: makes sure values are filled
# mycurser.execute("CREATE TABLE Games (gameID INT PRIMARY KEY, away_team INT, home_team INT,"
#                  "away_score INT, home_score INT, away_xR FLOAT, home_xR FLOAT, winner INT,"
#                  "FOREIGN KEY (away_team) REFERENCES Team(teamID),FOREIGN KEY (home_team) REFERENCES Team(teamID),"
#                  "FOREIGN KEY (winner) REFERENCES Team(teamID))")

# mycurser.execute("DESCRIBE Games")
# for x in mycurser:
#     print(x)


def retrieve_game_id():
    mycurser.execute("SELECT gameID FROM Games")
    ids = []
    for x in mycurser:
        id = int(x[0])
        ids.append(id)
    return ids


def retrieve_teamids():
    mycurser.execute("SELECT teamID FROM Team")
    ids = []
    for x in mycurser:
        id = int(x[0])
        ids.append(id)
    return ids


def add_game(gameID, away_id, home_id, away_score, home_score, away_xR, home_xr, winner, year, month, date):
    # if mycurser.execute("SELECT EXISTS(SELECT * FROM Games WHERE gameID=%s)", (gameID,)) == 0:
    print('adding game', gameID, year, month)
    mycurser.execute("INSERT INTO Games (gameID, away_team, home_team, away_score, home_score, away_xR, home_xR, winner, year, month, day)"
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (gameID, away_id, home_id, away_score, home_score, away_xR, home_xr, winner, year, month, date))
    db.commit()
    # else:
    #     print('not adding game', gameID, year, month)


def add_team(id, name, nickname):
    mycurser.execute("INSERT INTO Team (teamID, city_name, nickname) VALUES (%s, %s, %s)", (id, name, nickname))
    db.commit()


def add_basepaths(id):
    mycurser.execute("INSERT INTO Basepaths (basepathsID, zero_runs, one_runs, two_runs, three_runs, four_runs) VALUES (%s, %s, %s, %s, %s, %s)", (id, 0,0,0,0,0))
    db.commit()


def get_xr_basepath(id):
    sql = "SELECT * FROM Basepaths WHERE basepathsID = %s"
    mycurser.execute(sql, (id,))
    values, total = [], 0
    for x in mycurser:
        for y in x:
            if isinstance(y, int):
                values.append(y)
                total += y
    if total == 0:
        return 0
    else:
        prob0, prob1, prob2, prob3, prob4 = values[0]/total, values[1]/total, values[2]/total, values[3]/total, values[4]/total
        return prob0 * 0 + prob1 * 1 + prob2 * 2 + prob3 *3 + prob4*4


def get_run_value(id, run):
    if run == 0:
        sql = "SELECT zero_runs FROM Basepaths WHERE basepathsID = %s"
        mycurser.execute(sql, (id,))
        for x in mycurser:
            for y in x:
                return y
    elif run == 1:
        sql = "SELECT one_runs FROM Basepaths WHERE basepathsID = %s"
        mycurser.execute(sql, (id,))
        for x in mycurser:
            for y in x:
                return y
    elif run == 2:
        sql = "SELECT two_runs FROM Basepaths WHERE basepathsID = %s"
        mycurser.execute(sql, (id,))
        for x in mycurser:
            for y in x:
                return y
    elif run == 3:
        sql = "SELECT three_runs FROM Basepaths WHERE basepathsID = %s"
        mycurser.execute(sql, (id,))
        for x in mycurser:
            for y in x:
                return y
    elif run == 4:
        sql = "SELECT four_runs FROM Basepaths WHERE basepathsID = %s"
        mycurser.execute(sql, (id,))
        for x in mycurser:
            for y in x:
                return y


def update_basepath_runs(id, runs):
    value = get_run_value(id, runs) + 1
    if runs == 0:
        mycurser.execute("UPDATE Basepaths SET zero_runs = %s WHERE basepathsID = %s", (value, id))
    elif runs == 1:
        mycurser.execute("UPDATE Basepaths SET one_runs = %s WHERE basepathsID = %s", (value, id))
    elif runs == 2:
        mycurser.execute("UPDATE Basepaths SET two_runs = %s WHERE basepathsID = %s", (value, id))
    elif runs == 3:
        mycurser.execute("UPDATE Basepaths SET three_runs = %s WHERE basepathsID = %s", (value, id))
    elif runs == 1:
        mycurser.execute("UPDATE Basepaths SET four_runs = %s WHERE basepathsID = %s", (value, id))
    db.commit()


def get_expected_runs_for_team(id):
    pass


def get_xR_all_teams():
    # get team ids
    # loop over teamids
        # call get_expected_runs_for_team() and add value to dict
    # return dict
    pass


# add_basepaths('0')
# print(get_xr_basepath('0'))
# update_basepath_runs('0', 2)

# add elements
# mycurser.execute("INSERT INTO Person (name, age) VALUES (%s, %s)", ("Tim", 19))
# db.commit()

# add_team(1, 'test', 'hey')

# retrieve items
# * = all items, SELECT * FROM ____ WHERE: selects values, ORDER BY
# mycurser.execute("SELECT * FROM Games")
# for x in mycurser:
#     print(x)

# add a column to table
# DROP removes column, CHANGE prev_name new_name TYPE: changes col name
# mycurser.execute("ALTER TABLE Team CHANGE teamID INT PRIMARY KEY")
# db.commit()

# mycurser.execute("DELETE FROM Games")
# db.commit()
# mycurser.execute("ALTER/ TABLE Games ADD year INT")
# mycurser.execute("ALTER/ TABLE Games ADD year INT")
# mycurser.execute("ALTER TABLE Games ADD month INT")
# mycurser.execute("ALTER TABLE Games ADD day INT")

# mycurser.execute("DESCRIBE Games")
# for x in mycurser:
#     print(x)
# mycurser.execute("DELETE FROM Basepaths")

# mycurser.execute("SELECT * FROM Basepaths")
# index = 0
# for x in mycurser:
#     print(x)
#     index += 1
# print(index)
