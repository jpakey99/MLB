from PIL import Image, ImageDraw, ImageFont
from team_batting_stats import TeamBattingStats
from team_pitching_stats import TeamPitchingStats
from labels import MLBLabel
from team_stats import *
import database
from abrstract_graph import AbstractScatterGraph, AbstractGraph
from statistics import stdev
from Graph import *


WIDTH, HEIGHT = 1920,1028


class TeamStatViz(AbstractScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str, title, credits, subtitle, corner_labels):
        super().__init__(title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.batting_stats:TeamBattingStats = team_stats[0]
        self.pitching_stats:TeamPitchingStats = team_stats[1]
        # self.year = int(date.split('-')[2])

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
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str, title, credits, subtitle, corner_labels):
        super().__init__(team_stats, title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)


class TeamOverall(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Team Overall'
        credits = 'Twitter: @jpakey99, Idea: @CChartingHockey\n data: Fangraphs'  #Fine tone centering 2nd line
        corner_labels = ('good', 'dull', 'fun', 'bad')
        super().__init__(team_stats, date, title=title, subtitle=subtitle, credits=credits, corner_labels=corner_labels)
        self.axis_labels =  ('wRC+', 'xFIP-')
        self.wrc = self.batting_stats.wrc_adjusted()
        self.fip = self.pitching_stats.xfip_adjusted()
        combined, x, y, labels = self.combine_lists(self.fip, self.wrc)
        self.logos = self.labels.get_labels(labels)
        self.graph = Graph2DScatter(y, x, self.logos, self.axis_labels ,inverty=True)
        self.graph_size = (0, 0)

    def save_image(self):
        self.image.save('graphs//' + 'Team_Tiers' + '_' + self.date + '.png')


class TeamLuckGraph(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Team Luck'
        credits = 'Twitter: @jpakey99, Idea: @CChartingHockey, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Hitter BAPIP+', 'Pitcher BAPIP+')
        super().__init__(team_stats,title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.b_babip = self.batting_stats.babip_adjusted()
        self.p_babip = self.pitching_stats.babip_adjusted()
        combined, x, y, labels = self.combine_lists(self.b_babip, self.p_babip)
        self.logos = self.labels.get_labels(labels)
        self.graph = Graph2DScatter(y, x, self.logos, self.axis_labels, inverty=False)

    def save_image(self):
        self.image.save('graphs//' + 'Team_luck' + '_' + self.date + '.png')


class TeamRecordVsRunDif(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Win % vs Run Differential'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Run Differential', 'Winning Percentage')
        super().__init__(team_stats,title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.runs_for, self.runs_against = self.batting_stats.runs(), self.pitching_stats.runs()
        self.dif = self.get_run_diff() # get z-score for run dif
        self.wper = TeamStandings(2021).get_standings()
        combined, x, y, logos = self.combine_lists(self.dif, self.wper)
        x_axis = []
        self.graph = Graph2DScatter(x, y, logos, self.axis_labels, inverty=False, diag_lines=False, average_lines=True, best_fit=True)
        self.graph_size = (0,0)

    def combine_lists(self, list1, list2):
        combined, x, y, labels = [], [], [], []
        for diff_team, diff in list1:
            tm = database.get_name_from_abbr(diff_team)[0]
            if tm.split(' ')[-1] == 'Sox' or tm.split(' ')[-1] == 'Jays':
                s_team = tm.split(' ')[-2] + ' ' + tm.split(' ')[-1]
            else:
                s_team = tm.split(' ')[-1]
            for wp_team, wp in list2:
                if s_team in wp_team:
                    combined.append((diff, wp))
                    x.append(diff)
                    y.append(float(wp))
                    labels.append(diff_team)
        return combined, x, y, self.labels.get_labels(labels)

    def get_run_diff(self):
        diff, teams = [], []
        for bteam in self.runs_for:
            for pteam in self.runs_against:
                if bteam[0] == pteam[0]:
                    diff.append((bteam[0], bteam[1]-pteam[1]))
        return diff

    def save_image(self):
        self.image.save('graphs//' + 'W%vRunDiff' + '_' + self.date + '.png')


class RAvRF(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Runs Against vs Runs For'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Runs For', 'Runs Against')
        super().__init__(team_stats,title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.runs_for, self.runs_against = self.batting_stats.runs(), self.pitching_stats.runs()
        combined, x, y, logos = self.combine_lists(self.runs_for, self.runs_against)
        labels = self.labels.get_labels(logos)
        self.graph = Graph2DScatter(x, y, labels, self.axis_labels, inverty=True, diag_lines=True, average_lines=True, size=(12.2,12))
        self.graph_size = (0,0)

    def save_image(self):
        self.image.save('graphs//' + 'RAvRF' + '_' + self.date + '.png')


class xRAvxRF(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Run Expectancy Against vs\nRun Expectancy For'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Run Expectancy For', 'Run Expectancy Against')
        super().__init__(team_stats, title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.runs_for, self.runs_against = self.batting_stats.xruns(), self.pitching_stats.xruns()
        combined, x, y, logos = self.combine_lists(self.runs_for, self.runs_against)
        labels = self.labels.get_labels(logos)
        self.graph = Graph2DScatter(x, y, labels, self.axis_labels, inverty=False, diag_lines=True, average_lines=True)
        self.graph_size = (0,0)

    def save_image(self):
        self.image.save('graphs//' + 'xRAvXRF' + '_' + self.date + '.png')


class xRFvRF(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Runs For vs\nRuns For Over Expected'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Runs For Over Expected', 'Runs For')
        super().__init__(team_stats, title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.xruns_for, self.runs = self.batting_stats.xruns(), self.batting_stats.runs()
        combined, x, y, logos = self.combine_lists(self.xruns_for, self.runs)
        labels = self.labels.get_labels(logos)
        self.graph = Graph2DScatter(x, y, labels, self.axis_labels, inverty=False, diag_lines=False, average_lines=True, best_fit=True)
        self.graph_size = (0,0)

    def save_image(self):
        self.image.save('graphs//' + 'RFvXRF' + '_' + self.date + '.png')


class xRAvRA(TeamScatterGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Runs Against vs\nRuns Against Over Expected'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        corner_labels, self.axis_labels = ('good', 'dull', 'fun', 'bad'), ('Runs Against Over Expected', 'Runs Against')
        super().__init__(team_stats, title=title, credits=credits, subtitle=subtitle, date=date, corner_labels=corner_labels)
        self.xruns_against, self.runs_against = self.pitching_stats.xruns(), self.pitching_stats.runs()
        combined, x, y, logos = self.combine_lists(self.xruns_against, self.runs_against)
        labels = self.labels.get_labels(logos)
        self.graph = Graph2DScatter(x, y, labels, self.axis_labels, inverty=True, diag_lines=False, average_lines=True, best_fit=True)
        self.graph_size = (0,0)

    def save_image(self):
        self.image.save('graphs//' + 'RAvXRA' + '_' + self.date + '.png')


class TeamBarGraph(AbstractGraph):
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str, title, subtitle, credits):
        super().__init__(title=title, subtitle=subtitle, credits=credits, date=date)
        self.graph: BarGraph
        self.batting_stats, self.pitching_stats = team_stats


class RunDiff(TeamBarGraph):
    '''
    get actual run differential
    get RE24 run differential
    add the team with each
    create a list that is (team, rdiff, xrdiff)
    get color shade based on xrdiff
    '''
    def __init__(self, team_stats: [TeamBattingStats, TeamPitchingStats], date: str):
        subtitle = 'Updated: ' + date
        title = 'Team Run Differential'
        credits = 'Twitter: @jpakey99, data: Fangraphs'
        super().__init__(team_stats, title=title, subtitle=subtitle, credits=credits, date=date)
        self.runs_for, self.xruns_for = self.batting_stats.runs(), self.batting_stats.xruns()
        self.runs_against, self.xruns_against = self.pitching_stats.runs(), self.pitching_stats.xruns()
        self.combined_lists, self.diff, colors, self.team = self.combine()
        teams, values, colors = self.sort()
        logos = self.labels.get_labels(teams)
        self.graph = BarGraph(self.team, values, 'Run Differential', labels=logos, colors=colors)

    def combine(self):
        combined, diff, self.xdiff, team = [], [], [], []
        for item in self.runs_for:
            team_rf = item[0]
            for i in self.xruns_for:
                team_xrf = i[0]
                for j in self.runs_against:
                    team_ra = j[0]
                    for l in self.xruns_against:
                        team_xra = l[0]
                        if team_xra == team_ra == team_xrf == team_rf:
                            d = item[1] - j[1]
                            xd = i[1] + l[1]
                            # print(i[1]-l[1])
                            combined.append([d, xd, team_xra])
                            diff.append(d)
                            self.xdiff.append(xd)
                            team.append(team_xrf)
        colors = self.color_shade()
        for t in range(0, len(combined)):
            combined[t][1] = colors[t]
        return combined, diff, colors, team

    def color_shade(self):
        colors = []
        print(self.xdiff)
        m = max(max(self.xdiff), abs(min(self.xdiff)))
        for i in range(0,len(self.xdiff)):
            d = self.xdiff[i]
            if d < 0:
                r = 1
                g = b = 1 - abs(d / m)
            else:
                g = b = 1
                r = 1 - abs(d / m)
            colors.append((r,g,b))
        return colors

    def sort(self):
        for i in range(0, len(self.diff)):
            for j in range(0, len(self.diff)-1):
                if self.combined_lists[j][0] < self.combined_lists[j+1][0]:
                    temp = self.combined_lists[j]
                    # print(temp)
                    self.combined_lists[j] = self.combined_lists[j + 1]
                    self.combined_lists[j + 1] = temp
        teams, values, colors = [], [], []
        for value in self.combined_lists:
            teams.append(value[2])
            values.append(value[0])
            colors.append(value[1])
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


if __name__ == '__main__':
    g = RunDiff([TeamBattingStats(2021), TeamPitchingStats(2021)], '2190')
    # g = xBAvBA([TeamBattingStats(2021), TeamPitchingStats(2021)], '2190')
    g.create_image()
    g.save_image()