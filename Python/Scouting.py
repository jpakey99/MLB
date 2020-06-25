def create_dict(dict, player):
    dict[player] = {
        'position': '',
        'ab': 0,
        'hits' : 0,
        'bb': 0,
        'dbl': 0,
        'tpl': 0,
        'hr': 0
    }



def add_amatuer_player():
    amatuer_players = {}
    name = input("What is the player's name")
    create_dict(amatuer_players, name)
    position = input("What is the player's position")
    amatuer_players[name]['position'] = position
    ab = int(input("How many at bats does a player have"))
    amatuer_players[name]['ab'] = ab
    hits = int(input("How many hits does a player have"))
    amatuer_players[name]['hits'] = hits
    walks = int(input("How many walks does a player have"))
    amatuer_players[name]['bb'] = walks
    doubles = int(input("How many doubles does the player have"))
    amatuer_players[name]['dbl'] = doubles
    triples = int(input("How many triples does a player have"))
    amatuer_players[name]['tpl'] = triples
    hr = int(input("How many homeruns does a player have"))
    amatuer_players[name]['hr'] = hr
    return amatuer_players


def create_csv(filename):
    file = open(filename, 'w')
    header = 'name, position, at bats, hits, walks, doubles, triples, homeruns\n'
    file.write(header)
    file.close()


def add_to_csv(filename, dict):
    file = open(filename, 'a')
    buffer = ''
    for player in dict:
        buffer = buffer + player + ','
        for stat in dict[player]:
            buffer = buffer + str(dict[player][stat]) + ','
        file.write(buffer + '\n')
        buffer = ''
    file.close()


def main():
    apf = 'amatuer_players.csv'
    create_csv(apf)
    amatuer_players = {}
    run = True

    while run:
        user = input("1: Add amatuer players 0: Exit")
        if user == '1':
            amatuer_players = add_amatuer_player()
        else:
            break
    add_to_csv(apf, amatuer_players)


main()