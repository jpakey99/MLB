import datetime
from TeamViz import *

# TODO: change from data gettig being a subclass of a graph class to a graph class being a subclass of a data classk=
# TODO: load data from previous week
# TODO: make a gif that transitions from 1 set to next set of data
# TODO: individual Player cards
# TODO: individual Team Cards
WIDTH, HEIGHT = 1920,1028


def find_z_score(data, value):
    mean = 0
    for item in data:
        mean += item
    mean = mean/len(data)
    top = value - mean
    bottom = stdev(data)
    return top / bottom


def combine_lists(list1, list2):
    combined, x, y, labels = [], [], [], []
    for item in list1:
        team = item[0]
        for i in list2:
            t = i[0]
            if team == t:
                combined.append((team, item[1], i[1]))
                x.append(item[1])
                y.append(i[1])
                labels.append(team)
    return combined, x, y, labels


if __name__ == '__main__':
    pass