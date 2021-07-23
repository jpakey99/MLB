import pybaseball
from statistics import stdev


def get_stats(player):
    return player[10], player[1]


def read_file():
    file = open("prospects/fangraphs-the-board-data.csv")
    file.readline()
    a, aplus, aa, aaa = [], [], [], []
    for line in file:
        player = line.split(',')
        if player[3] == '"A"':
            a.append(get_stats(player))
        elif player[3] == '"A+"':
            aplus.append(get_stats(player))
        elif player[3] == '"AA"':
            aa.append(get_stats(player))
        elif player[3] == '"AAA"':
            aaa.append(get_stats(player))
    print(len(a), len(aplus), len(aa), len(aaa))


def find_z_score(self, data, value):
    mean = 0
    for item in data:
        mean += item
    mean = mean / len(data)
    top = value - mean
    bottom = stdev(data)
    return top / bottom


if __name__ == '__main__':
    read_file()