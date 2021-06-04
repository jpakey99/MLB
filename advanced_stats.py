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


class DataGraphs:
    def __init__(self, year):
        self.pitching_stats = TeamPitchingStats(year)
        self.batting_stats = TeamBattingStats(year)
        self.graph_image = None

    def graph_data(self):
        graph = self.graph.graph()
        time = datetime.datetime.now()
        string_time = time.strftime("%Y%m%d")
        graph.savefig('graphs//' + self.name+string_time, bbox_inches='tight')
        self.graph_image = graph

    def display_graph(self):
        self.graph_image.show()


class TeamOveralsl(DataGraphs):
    def __init__(self, year):
        super().__init__(year)
        self.name = 'team_overall_'
        self.wrc = self.batting_stats.wrc_adjusted()
        self.fip = self.pitching_stats.xfip_adjusted()
        combined, x, y, labels = combine_lists(self.fip, self.wrc)
        self.labels = MLBLabel().get_labels(labels)
        self.corner_labels = ('dull', 'good', 'bad', 'lucky')
        self.axis_labels = ('wRC+', 'xFIP-')
        self.title = 'wRC+ vs xFIP-'
        self.graph = Graph2DScatter(y, x, self.title, self.labels, self.axis_labels, corner_labels=self.corner_labels, inverty=True, credit=True)


class LuckGraph(DataGraphs):
    def __init__(self, year):
        super().__init__(year)
        self.name = 'luck_'
        self.batting_babip = self.batting_stats.babip_adjusted()
        self.pitching_babip = self.pitching_stats.babip_adjusted()
        combined, x, y, labels = combine_lists(self.pitching_babip, self.batting_babip)
        self.labels = MLBLabel().get_labels(labels)
        self.axis_labels = ('batting babip', 'pitching babip')
        self.title = 'Luck'
        self.graph = Graph2DScatter(y, x, self.title, self.labels, self.axis_labels, credit=False, inverty=True)


class RunDiffGraph(DataGraphs):
    def __init__(self, year):
        super().__init__(year)
        self.name = 'Run Diff_'
        self.scored = self.batting_stats.runs()
        self.givin_up = self.pitching_stats.runs()
        combined, ra, rf, labels = combine_lists(self.givin_up, self.scored)
        diff, self.combined = [], []
        for i in range(0, len(rf)):
            diff.append(rf[i] - ra[i])
            self.combined.append((labels[i], rf[i] - ra[i]))
        teams, y = self.sort()
        display =  MLBLabel()
        self.labels =display.get_labels(teams)
        self.colors = display.get_colors(teams)
        self.graph = BarGraph(teams, y, 'Run Differential', labels=self.labels, colors=self.colors)

    def sort(self):
        for i in range(0, len(self.combined)):
            for j in range(0, len(self.combined)-1):
                if self.combined[j][1] < self.combined[j+1][1]:
                    temp = self.combined[j]
                    self.combined[j] = self.combined[j+1]
                    self.combined[j+1] = temp

        teams, values = [], []
        for value in self.combined:
            teams.append(value[0])
            values.append(value[1])
        return teams, values


class Card:
    def __init__(self, year, team):
        self.name = 'graphs//Team Card_' + team + '_'
        self.pitching_stats = TeamPitchingStats(year)
        self.batting_stats = TeamBattingStats(year)
        self.graph1_image = None
        self.graph2_image = None
        self.image = None
        self.time = datetime.datetime.now()
        self.credits = 'Twitter: @jpakey99, Idea: Evolving Hockey, data: Fangraphs'

    def graph_data(self):
        string_time = self.time.strftime("%Y%m%d")
        title_time = self.time.strftime("%d/%m/%Y")
        w,h, y = 1920,1028,140
        font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        font1 = ImageFont.truetype('Roboto-Regular.ttf', 20)
        graph1 = self.graph1.graph()
        graph1.savefig('1', bbox_inches='tight')
        self.image = Image.new('RGB', (w, h))
        draw = ImageDraw.ImageDraw(self.image)
        draw.rectangle((0,0,w,h),fill=(255,255,255))
        draw.text((330,20), self.title, fill=(0,0,0), font=font)
        draw.text((280, 70), self.subtitle + title_time, fill=(0, 0, 0), font=font1)
        draw.text((150, 95), self.credits, fill=(0, 0, 0), font=font1)
        i1 = Image.open('1.png', 'r')
        self.image.paste(i1, box=(0,y))
        graph2 = self.graph2.graph()
        graph2.savefig('2', bbox_inches='tight')
        i2 = Image.open('2.png', 'r')
        self.image.paste(i2, box=(556,y))
        name = self.name + string_time + ".png"
        print(name)
        self.image.save(name)

    def display_graph(self):
        self.image.convert('RGB').show()


class TeamCard(Card):
    def __init__(self, year, team):
        super().__init__(year, team)
        self.team = team
        self.title = 'Team Card: ' + self.team
        self.subtitle = 'Team Overall Updated: '
        stats = []
        stat_line = ('wRC+', 'Hard%+', 'Soft%+', 'LD%+', 'babip+')
        stats.append(self.batting_stats.wrc_adjusted())
        stats.append(self.batting_stats.hard_adjusted())
        stats.append(self.batting_stats.soft_adjusted())
        stats.append(self.batting_stats.linedrive_adjusted())
        stats.append(self.batting_stats.babip_adjusted())
        team_stats, all_stat = [], []
        for i in range(0, len(stats)):
            all_stat = []
            for j in range(0, len(stats[i])):
                all_stat.append(stats[i][j][1])
                if stats[i][j][0] == self.team:
                    team_value = stats[i][j][1]
            team_stats.append(find_z_score(all_stat, team_value))
        self.graph1 = TeamCardGraph(stat_line, team_stats, 'TEAM CARD',xaxis=True)
        stats, team_stats, all_stat = [], [], []
        stat_line = ('xFIP-', 'Hard%+', 'Soft%+', 'HR/9+', 'babip+')
        stats.append(self.pitching_stats.xfip_adjusted())
        stats.append(self.pitching_stats.hard_adjusted())
        stats.append(self.pitching_stats.soft_adjusted())
        stats.append(self.pitching_stats.homerun_nine_adjusted())
        stats.append(self.pitching_stats.babip_adjusted())
        for i in range(0, len(stats)):
            all_stat = []
            for j in range(0, len(stats[i])):
                all_stat.append(stats[i][j][1])
                if stats[i][j][0] == self.team:
                    team_value = stats[i][j][1]
            team_stats.append(find_z_score(all_stat, team_value))
        self.graph2 = TeamCardGraph(stat_line, team_stats, 'TEAM CARD',xaxis=False)


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
    graphs = []
    graphs.append(TeamOverall(year))
    graphs.append(LuckGraph(year))
    graphs.append(RunDiffGraph(year))

    for graph in graphs:
        graph.graph_data()


if __name__ == '__main__':
    time = datetime.datetime.now()
    string_time = time.strftime("%m-%d-%Y")
    tps = TeamPitchingStats(2021)
    tbs = TeamBattingStats(2021)
    toc = TeamOverall([tbs, tps], string_time)
    toc.create_image()
    toc.display_image()
    toc.save_image()
    pass