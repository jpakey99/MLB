from labels import MLBLabel
from PIL import Image, ImageDraw, ImageFont
from team_batting_stats import TeamBattingStats
from team_pitching_stats import TeamPitchingStats
from labels import MLBLabel
from statistics import stdev
from Graph import *


WIDTH, HEIGHT = 1920,1028


class TeamStatViz:
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        self.batting_stats:TeamBattingStats = team_stats[0]
        self.pitching_stats:TeamPitchingStats = team_stats[1]
        self.date = date
        # self.year = int(date.split('-')[2])
        self.labels = MLBLabel()
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0,0,WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)

    def create_image(self):
        pass

    def save_image(self):
        pass

    def display_image(self):
        self.image.show()

    def combine_lists(self, list1, list2):
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

    def find_z_score(self, data, value):
        mean = 0
        for item in data:
            mean += item
        mean = mean / len(data)
        top = value - mean
        bottom = stdev(data)
        return top / bottom


class TeamCard(TeamStatViz):
    def __init__(self,  team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)


class TeamScatterGraph(TeamStatViz):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)


class TeamOverall(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)
        self.subtitle = 'Updated: ' + date
        self.title = 'Team Overall'
        self.credits = 'Twitter: @jpakey99, Idea: @CChartingHockey, data: Fangraphs'
        self.corner_labels =  ('wRC+', 'xFIP-')
        self.wrc = self.batting_stats.wrc_adjusted()
        self.fip = self.pitching_stats.xfip_adjusted()
        combined, x, y, labels = self.combine_lists(self.fip, self.wrc)
        self.logos = self.labels.get_labels(labels)
        self.graph = Graph2DScatter(y, x, self.logos, self.corner_labels ,inverty=True)

    def create_image(self):
        x, y = 100, 150
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        sw, th = self.draw.textsize(self.subtitle, font=self.sub_title_font)
        cw, th = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((WIDTH - tw)/2, 10), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((WIDTH - sw)/2, 70), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((WIDTH - cw)/2, 100), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        g : Image.Image = Image.open('1.png')
        x = WIDTH//2 - g.size[0]//2
        self.image.paste(g, box=(x, y))
        gx, gy = g.size
        self.draw.text((x + 100, y + 20), text='dull', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x + 100, gy + 30), text='bad', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((gx - 70, y + 20), text='good', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((gx - 70, gy + 30), text='fun', fill=(0, 0, 0, 255), font=self.sub_title_font)

    def save_image(self):
        self.image.save('graphs//' + 'Team_Tiers' + '_' + self.date + '.png')


class TeamLuckGraph(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)
        self.subtitle = 'Updated: ' + date
        self.title = 'Team Luck'
        self.credits = 'Twitter: @jpakey99, Idea: @CChartingHockey, data: Fangraphs'
        self.corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Hitter BAPIP+', 'Pitcher BAPIP+')
        self.b_babip = self.batting_stats.babip_adjusted()
        self.p_babip = self.pitching_stats.babip_adjusted()
        combined, x, y, labels = self.combine_lists(self.b_babip, self.p_babip)
        self.logos = self.labels.get_labels(labels)
        self.graph = Graph2DScatter(y, x, self.logos, self.axis_labels, inverty=False)

    def create_image(self):
        x, y = 20, 150
        tw, th = self.draw.textsize(self.title, font=self.title_font)
        sw, th = self.draw.textsize(self.subtitle, font=self.sub_title_font)
        cw, th = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((WIDTH - tw) / 2, 10), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((WIDTH - sw) / 2, 70), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((WIDTH - cw) / 2, 100), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        g :Image.Image= Image.open('1.png')
        gx, gy = g.size
        self.image.paste(g, box=(x, y))
        self.draw.text((x+100, y+20), text='dull', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x + 100, gy+30), text='bad', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((gx-70, y + 20), text='good', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((gx-70, gy + 30), text='fun', fill=(0, 0, 0, 255), font=self.sub_title_font)

    def save_image(self):
        self.image.save('graphs//' + 'Team_luck' + '_' + self.date + '.png')


class TeamBarGraph(TeamStatViz):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)
        self.graph: BarGraph


class RunDiff(TeamBarGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)
        self.subtitle = 'Updated: ' + date
        self.title = 'Team Run Differential'
        self.credits = 'Twitter: @jpakey99, Idea: @ChartingHockey, data: Fangraphs'
        self.scored = self.batting_stats.runs()
        self.given_up = self.pitching_stats.runs()
        combined, self.ra, self.rf, self.t_a = self.combine_lists(self.given_up, self.scored)
        self.diff = self.get_graph_values()
        self.combined = self.color_shade()
        teams, y, colors = self.sort()
        self.logos = self.labels.get_labels(teams)
        print(teams)
        self.graph = BarGraph(teams, y, 'Run Differential', labels=self.logos, colors=colors)

    def color_shade(self):
        combined = []
        m = max(max(self.diff), abs(min(self.diff)))
        for i in range(0,len(self.diff)):
            d = self.diff[i]
            r, g, b = 0, 0, 0
            if d < 0:
                r = 1
                g = b = 1 - abs(d / m)
            else:
                g = b = 1
                r = 1 - abs(d / m)
            combined.append((self.t_a[i], d, (r,g,b)))
        return combined

    def get_graph_values(self):
        diff= []
        for i in range(0,len(self.rf)):
            diff.append(self.rf[i] - self.ra[i])
        return diff

    def sort(self):
        for i in range(0, len(self.combined)):
            for j in range(0, len(self.combined) - 1):
                if self.combined[j][1] < self.combined[j + 1][1]:
                    temp = self.combined[j]
                    self.combined[j] = self.combined[j + 1]
                    self.combined[j + 1] = temp

        teams, values, colors = [], [], []
        for value in self.combined:
            teams.append(value[0])
            values.append(value[1])
            colors.append(value[2])
        return teams, values, colors

    def create_image(self):
        y = 170
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        sw, th = self.draw.textsize(self.subtitle, font=self.sub_title_font)
        cw, th = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((WIDTH - tw)/2, 10), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((WIDTH - sw)/2, 70), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((WIDTH - cw)/2, 100), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        self.image.paste(Image.open('1.png'), box=(20, y))

    def save_image(self):
        self.image.save('graphs//' + 'Run_Diff' + '_' + self.date + '.png')


class TeamOverallCard(TeamCard):
    def __init__(self, team,  team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        super().__init__(team_stats, date)
        self.team = team
        self.graph1_stat_line = ('wRC+', 'Hard%+', 'Soft%+', 'LD%+', 'babip+')
        self.graph2_stat_line = ('xFIP-', 'Hard%+', 'Soft%+', 'HR/9+', 'babip+')
        self.subtitle = 'Left: BattingTeam, Right: Pitching, Updated: ' + date
        self.title = 'Team Card: ' + self.team
        self.credits = 'Twitter: @jpakey99, Idea: Evolving Hockey, data: Fangraphs'
        self.label = self.labels.logos[self.team]
        self.b_stats, self.p_stats = [], []
        self.b_stats.append(self.batting_stats.wrc_adjusted())
        self.b_stats.append(self.batting_stats.hard_adjusted())
        self.b_stats.append(self.batting_stats.soft_adjusted())
        self.b_stats.append(self.batting_stats.linedrive_adjusted())
        self.b_stats.append(self.batting_stats.babip_adjusted())
        self.p_stats.append(self.pitching_stats.xfip_adjusted())
        self.p_stats.append(self.pitching_stats.hard_adjusted())
        self.p_stats.append(self.pitching_stats.soft_adjusted())
        self.p_stats.append(self.pitching_stats.homerun_nine_adjusted())
        self.p_stats.append(self.pitching_stats.babip_adjusted())
        self.team_batting_stats = self.get_team_stats(self.b_stats)
        self.team_pitching_stats = self.get_team_stats(self.p_stats)
        self.graph1 = TeamCardGraph(self.graph1_stat_line, self.team_batting_stats, self.title, False, False)
        self.graph2 = TeamCardGraph(self.graph2_stat_line, self.team_pitching_stats, self.title, False, False)

    def get_team_stats(self, stats):
        team_stats, all_stat = [], []
        for i in range(0, len(stats)):
            all_stat = []
            for j in range(0, len(stats[i])):
                all_stat.append(stats[i][j][1])
                if stats[i][j][0] == self.team:
                    team_value = stats[i][j][1]
            team_stats.append(self.find_z_score(all_stat, team_value))
        return team_stats

    def create_image(self):
        y = 140
        self.draw.text((800, 10), text=self.title, fill=(0,0,0, 255), font=self.title_font)
        self.draw.text((650, 70), text=self.subtitle, fill=(0,0,0, 255), font=self.sub_title_font)
        self.draw.text((600, 100), text=self.credits, fill=(0,0,0, 255), font=self.sub_title_font)
        i: Image.Image = Image.open(self.label)
        # i.convert('RGB')
        i.thumbnail((120,120))
        self.image.alpha_composite(i, dest=(450,10))
        # self.image.paste(i, box=(450,10))
        self.graph1.graph().savefig('1', bbox_inches='tight')
        self.image.paste(Image.open('1.png'), box=(40, y))
        self.graph2.graph().savefig('2', bbox_inches='tight')
        self.image.paste(Image.open('2.png'), box=(1000, y))

    def save_image(self):
        self.image.save('graphs//' + 'Team Card_'+ self.team + '_' + self.date + '.png')


def img_creator(image):
    for x in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = (x, j)
            color = image.getpixel(pixel)
            if color[0] <= 30 and color[1] <= 30 and color[2] <= 30:
                image.putpixel(pixel, (255, 255, 255))
    return image


