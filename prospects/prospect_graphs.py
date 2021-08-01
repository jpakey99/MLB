from prospects.prospects import read_file
from Graph import *
import numpy as np
from abrstract_graph import *
import os

WIDTH, HEIGHT = 1920,1028

Season,Name,Team,Level,Age,G,PA,AVG,BBP,KP,ISO,BABIP,wRAA,wOBA,wRCa,LDP,GBP,FBP,PullP,CentP,OppoP,SwStrP,Pitches,PlayerId = range(0, 24)

# for leagues of the same level: get mean, std, and z_score of that league but combine on 1 graph
# Ability to show 1 or more teams
# Ability to filter by age, games, plate appearances, position


class ProspectGraphAbstract(AbstractScatterGraph):
    def __init__(self, title, credits, subtitle, date, corner_labels):
        super().__init__(title, credits, subtitle, date, corner_labels)
        # self.year = int(date.split('-')[2])
        self.labels = MLBLabel()
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.x, self.zx = [], []
        self.y, self.zy = [], []
        self.team, self.name = [], []
        self.stat1, self.stat2 = [], []

    def add_prospect(self, prospect, stat1, stat2):
        self.team.append(prospect[2].strip('"'))
        self.name.append(prospect[1].strip('"'))
        self.y.append(float(prospect[stat1]))
        self.x.append(float(prospect[stat2]))

    def get_data(self, stat1, stat2, year, level, show_teams=None, all=False):
        for file in os.listdir('prospects/batting_data/'):
            file_level = file.split('_')[0]
            if level == file_level:
                prospects = read_file('prospects/batting_data/' + file)
                for prospect in prospects:
                    games, pa = int(prospect[G]), int(prospect[PA])
                    if games > 20 and pa / games > 1:
                        self.stat1.append(float(prospect[stat1]))
                        self.stat2.append(float(prospect[stat2]))
                        if show_teams is None:
                            if int(prospect[0]) == int(year) or all:
                                self.add_prospect(prospect, stat1, stat2)
                        elif prospect[2].strip('"') in show_teams:
                            if int(prospect[0]) == int(year) or all:
                                self.add_prospect(prospect, stat1, stat2)
                self.average = (np.mean(self.x), np.mean(self.y))
                for i in range(0, len(self.x)):
                    self.zx.append(self.find_z_score(self.average[0], self.x[i], self.x))
                    self.zy.append(self.find_z_score(self.average[1], self.y[i], self.y))
                self.x, self.y = [], []

    def find_z_score(self, mean, value, data):
        top = value - mean
        bottom = stdev(data)
        return top / bottom


class WalkRateVsWRAA(ProspectGraphAbstract):
    def __init__(self, date: str, show_teams=None, all=False):
        title = 'Walk % Vs wRAA'
        corner_labels = ('', '', '', '')
        subtitle = '2021 AA East'
        credits = 'Twitter: @jpakey99, Idea: @ShutdownLine\n data: Fangraphs'
        super().__init__(title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.get_data(BBP, wRAA, date, 'AA', show_teams=show_teams, all=all)
        labels = MLBLabel().get_labels(self.team)
        avg = (np.mean(self.zx), np.mean(self.zy))
        print(len(self.zx), len(self.zy), len(labels))
        self.graph = Graph2DScatter(self.zx, self.zy,labels=labels, axis_labels=['wRAA', 'Walk%'], average_lines=True, inverty=False, invertx=False, diag_lines=False, dot_labels=self.name, average=avg)


class WalkRateVsAge(ProspectGraphAbstract):
    def __init__(self, date, level, show_teams=None, all=False):
        title = 'Walk Rate Vs Age'
        corner_labels = ('', '', '', '')
        subtitle = '2021 AA East'
        credit = 'Twitter: @jpakey99, Idea: @ShutdownLine\n data: Fangraphs'
        super().__init__(title, credit, subtitle, date, corner_labels)
        self.get_data(Age, BBP, date, level, show_teams=show_teams, all=all)
        labels = MLBLabel().get_labels(self.team)
        avg = (np.mean(self.zx), np.mean(self.zy))
        print(len(self.zx), len(self.zy), len(labels))
        self.graph = Graph2DScatter(self.zx, self.zy, labels=labels, axis_labels=['Walk% z-score', 'Age z-score'], average_lines=True, inverty=True, invertx=False, diag_lines=True, dot_labels=self.name,
                                    average=avg)


if __name__ == '__main__':
    prospects = read_file('AAA_East.csv')
    walk_rate, wRAA, team = [], [], []
    for prospect in prospects:
        walk_rate.append(float(prospect[9]))
        wRAA.append(float(prospect[12]))
        team.append(prospect[2].strip('"'))
    labels = MLBLabel().get_labels(team)
    g = WalkRateVsWRAA(wRAA, walk_rate, labels, '1011')
    g.create_image()
    g.image.show()
