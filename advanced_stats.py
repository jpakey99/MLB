from team_batting_stats import TeamBattingStats
from team_pitching_stats import TeamPitchingStats
from labels import MLBLabel
import datetime
from Graph import *
from statistics import stdev
from PIL import Image, ImageDraw, ImageFont
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


def save_data(data, buffer):
    time = datetime.datetime.now()
    string_time = time.strftime("%Y%m%d") + '.csv'
    file = open(string_time, 'w')
    file.write(buffer + '\n')
    for line in data:
        string = ''
        for item in line:
            string += str(item) + ','
        string += '\n'
        file.write(string)


def run_all_graphs(year):
    time = datetime.datetime.now()
    string_time = time.strftime("%m-%d-%Y")
    tps = TeamPitchingStats(2021)
    tbs = TeamBattingStats(2021)
    toc = TeamOverall([tbs, tps], string_time)
    toc.create_image()
    # toc.display_image()
    toc.save_image()

    tluck = TeamLuckGraph([tbs, tps], string_time)
    tluck.create_image()
    # tluck.display_image()
    tluck.save_image()

    trun_diff = RunDiff([tbs, tps], string_time)
    trun_diff.create_image()
    # trun_diff.display_image()
    trun_diff.save_image()


if __name__ == '__main__':
    run_all_graphs(2021)