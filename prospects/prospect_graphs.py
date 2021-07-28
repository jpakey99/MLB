from prospects.prospects import read_file
from Graph import *
import numpy as np
from abrstract_graph import *

WIDTH, HEIGHT = 1920,1028


# for leagues of the same level: get mean, std, and z_score of that league but combine on 1 graph
# Ability to show 1 or more teams
# Ability to filter by age, games, plate appearances, position


class ProspectGraph(ScatterGraph):
    def __init__(self, x, y, title, credits, subtitle, date, corner_labels):
        super().__init__(title, credits, subtitle, date, corner_labels)
        # self.year = int(date.split('-')[2])
        self.labels = MLBLabel()
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.x = x
        self.y = y


class WalkRateVsWRAA(ProspectGraph):
    def __init__(self, date: str, show_teams=None):
        prospects = read_file('prospects/AAA_East.csv')
        walk_rate, wRAA, team, name, x, y = [], [], [], [], [], []
        for prospect in prospects:
            walk_rate.append(float(prospect[9]))
            wRAA.append(float(prospect[12]))
            if show_teams == None:
                team.append(prospect[2].strip('"'))
                name.append(prospect[1].strip('"'))
                y.append(float(prospect[9]))
                x.append(float(prospect[12]))
            elif prospect[2].strip('"') in show_teams:
                team.append(prospect[2].strip('"'))
                name.append(prospect[1].strip('"'))
                y.append(float(prospect[9]))
                x.append(float(prospect[12]))
        labels = MLBLabel().get_labels(team)
        title = 'Walk % Vs wRAA'
        corner_labels = ('', '', '', '')
        subtitle = '2021 AAA East'
        credits = 'Twitter: @jpakey99, Idea: @ShutdownLine\n data: Fangraphs'  #Fine tone centering 2nd line
        super().__init__(x, y, title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.average =(np.mean(wRAA), np.mean(walk_rate))
        print(len(self.x), len(self.y), len(labels))
        self.graph = Graph2DScatter(self.x, self.y,labels=labels, axis_labels=['wRAA', 'Walk%'], average_lines=True, inverty=False, invertx=False, diag_lines=False, dot_labels=name, average=self.average)


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
