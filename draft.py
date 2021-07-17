import os
import draft_database
# from draft import draft_database
from labels import MLBLabel
from Graph import *
from PIL import Image, ImageDraw, ImageFont
import statsapi, pybaseball


WIDTH, HEIGHT = 1920,1028


def read_pool_files():
    for file_name in os.listdir("draft/Bonus Pools"):
        if file_name.endswith('.tsv'):
            year = file_name.split('- ')[1].split('.')[0]
            print(year)
            file = open("draft/Bonus Pools/" + file_name)
            file.readline()
            for line in file:
                team_pool = line.split('\t')
                tm = draft_database.get_teamID_from_nickname(team_pool[0])
                s = team_pool[1].split(',')
                pool_s = ''
                for c in s:
                    pool_s += c
                pool = int(pool_s)
                picks = int(team_pool[2])
                draft_database.add_pool(tm, pool, picks, year)


def read_all_files():
    for file_name in os.listdir("draft/MLB DRAFT"):
        if file_name.endswith('.txt'):
            print(file_name)
            file = open("draft/MLB DRAFT/" + file_name)
            file.readline()

            for line in file:
                if "Year" in line or line == ' ':
                    print(line)
                else:
                    selection = line.split(',')
                    if selection[6] == 'Y':
                        year = int(selection[0])
                        d_round = int(selection[1].strip('s'))
                        o_pick = int(selection[3])
                        r_pick = int(selection[4])
                        print(selection[5])
                        tm = draft_database.get_teamID_from_nickname(selection[5])
                        if selection[7] != '':
                            bonus = int(selection[7].strip('$'))
                        else:
                            bonus = 0
                        pos = selection[9]
                        if selection[10] != '':
                            war = float(selection[10])
                        else:
                            war = 0
                        pos = selection[9]
                        if pos in ['LHP', 'RHP']:
                            if selection[16] == '':
                                games = 0
                            else:
                                games = int(selection[16])
                        else:
                            if selection[11] == '':
                                games = 0
                            else:
                                games = int(selection[11])
                        ty = selection[-2]
                        name = selection[8].split('(')[0]
                        name = name.strip('*').split(' ')
                        f_name = name[0]
                        l_name = ''
                        for n in name[1:]:
                            l_name += n
                        l_name.strip(' ')
                        # print(d_round, year, o_pick, r_pick, tm, f_name, l_name, war, games, bonus, type, pos)
                        draft_database.add_draft_pick(round=d_round, year=year, pick_num_round=r_pick, pick_overall=o_pick, selection_team=tm, player_first_name=f_name, player_last_name=l_name, WAR=war, games_played=games, bonus=bonus, type=ty, position=pos)
                        # draft_database.add_draft_pick(d_round, year, r_pick, o_pick, tm, f_name, l_name, war, games, bonus, ty, pos)


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


def run_war_vs_players_graph():
    teams = draft_database.retrieve_teamids()
    war, games = [], []
    for team in teams:
        war.append((team, draft_database.get_draft_pick_war_per_team_year_year(team, 2012)))
        games.append((team, draft_database.get_total_mlb_players_from_team_draft_year(team, 2012)))
    combined, x, y, labels = combine_lists(war, games)
    mlb_labels = MLBLabel()
    l = mlb_labels.get_labels_by_id(labels)
    print(x, y, labels)
    graph = Graph2DScatter(x, y, l, ('war', 'players reach majors'), False, False, False)
    graph.graph().show()


class PlayersVsProduction:
    def __init__(self, year):
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 100)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.title = str(year) + ' Draft'
        self.credits = 'Twitter: @jpakey99, data: baseball_reference'
        self.year = year
        teams = draft_database.retrieve_teamids()
        self.war, self.games = [], []
        for team in teams:
            self.war.append((team, draft_database.get_draft_pick_war_per_team_year_year(team, year)))
            self.games.append((team, draft_database.get_total_mlb_players_from_team_draft_year(team, year)))
        combined, x, y, labels = combine_lists(self.war, self.games)
        mlb_labels = MLBLabel()
        l = mlb_labels.get_labels_by_id(labels)
        print(x, y, labels)
        self.graph = Graph2DScatter(x, y, l, ('WAR/162', 'Number of Players Who Reached Majors'), True, False, False, size=(12, 12), diag_lines=False)

    def create_image(self):
        x, y = 800, 20
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        cw, ch = self.draw.textsize(self.credits, font=self.sub_title_font)
        text_box = WIDTH -800
        self.draw.text((((text_box-tw)/4), (HEIGHT/2)-th), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text((((text_box-cw)/5), (HEIGHT/2)+ch), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        g: Image.Image = Image.open('1.png')
        gx, gy = g.size
        print(x+100, y+gy)
        self.image.paste(g, box=(x, y))
        self.draw.text((x+100, y + 20), text='many players\nlittle production', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+100, gy-100), text='bad', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+gx-100, y + 20), text='good', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+gx-250, gy-130), text='lot of production\nlittle players', fill=(0, 0, 0, 255), font=self.sub_title_font)

    def save_image(self):
        self.image.save('draft//' + 'draft' + 'games_vs_production_' + str(self.year) + '.png')


class PoolVsProduction:
    def __init__(self, year):
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 100)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.title = str(year) + ' Draft'
        self.sub_title = 'Bonus Pool per Draft Pick vs Production'
        self.credits = 'Twitter: @jpakey99, data: baseball_reference'
        self.year = year
        teams = draft_database.retrieve_teamids()
        self.war, self.games = [], []
        for team in teams:
            self.war.append((team, draft_database.get_draft_pick_war_per_team_year_year(team, year)))
            self.games.append((team, draft_database.get_pool_per_pick(team, year)))
        print(self.war, self.games)
        combined, x, y, labels = combine_lists(self.war, self.games)
        mlb_labels = MLBLabel()
        l = mlb_labels.get_labels_by_id(labels)
        # print(x, y, labels)
        self.graph = Graph2DScatter(x, y, l, ('WAR/162', 'Bonus Pool per Pick ($100,000'), True, False, False, size=(12, 12), diag_lines=False)

    def create_image(self):
        x, y = 800, 20
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        sw, sh = self.draw.textsize(self.sub_title, font=self.sub_title_font)
        cw, ch = self.draw.textsize(self.credits, font=self.sub_title_font)
        text_box = WIDTH -800
        self.draw.text((((text_box-tw)/4), (HEIGHT/2)-th), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text((((text_box - sw) / 5), (HEIGHT / 2) +sh), text=self.sub_title, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((((text_box-cw)/5), (HEIGHT/2)+(2*ch)), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        g: Image.Image = Image.open('1.png')
        gx, gy = g.size
        print(x+100, y+gy)
        self.image.paste(g, box=(x, y))
        self.draw.text((x+100, y + 20), text='spent lots\nlittle production', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+100, gy-130), text='spent little\nlittle production', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+gx-160, y + 20), text='fair value', fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((x+gx-160, gy-100), text='great value', fill=(0, 0, 0, 255), font=self.sub_title_font)

    def save_image(self):
        self.image.save('draft//' + 'draft' + 'pool_vs_production' + str(self.year) + '.png')


class War_per_162_per_pick:
    def __init__(self):
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.graph : BarGraph
        self.title = 'War per 162 of First Round Picks since 2012'
        self.credits = 'Twitter: @jpakey99, data: baseball_reference'
        self.war, self.picks = [], []
        for i in range(1, 31):
            self.war.append(draft_database.get_war_per_162_for_pick(i))
            self.picks.append(i)
        print(self.picks, self.war)
        colors = self.color_shade()
        self.graph = BarGraph(self.picks, self.war, 'War per 162', x_ticks=True, colors=colors, y_label='WAR/162')
        # self.graph.graph().show()

    def color_shade(self):
        colors = []
        m = max(max(self.war), abs(min(self.war)))
        for i in range(0,len(self.war)):
            d = self.war[i]
            r, g, b = 0, 0, 0
            if d/5 <.5:
                r = 1
                g = b = 1 - abs(d / m)
            else:
                g = b = 1
                r = 1 - abs(d / m)
            colors.append((r,g,b))
        return colors

    def create_image(self):
        y = 160
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        cw, th = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((WIDTH - tw)/2, 10), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((WIDTH - cw)/2, 100), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        self.image.paste(Image.open('1.png'), box=(20, y))

    def save_image(self):
        self.image.save('draft//' + 'draft' + '_war_per_162' + '.png')



def main():
    # read_pool_files()
    # read_all_files()
    graph = PoolVsProduction(2016)
    graph.create_image()
    graph.save_image()

    # draft using pybaseball
    # round = pybaseball.amateur_draft(2014, 1)
    # picks = []
    # for i in range(0, len(round)):
    #     print(i, round['Tm'][i], round['OvPck'][i])
        # picks.append((round['Tm'][i], round['OvPck'][i], round['Name'][i], round['Pos'][i], round['Signed'][i], round['WAR'][i]))
    # print(picks)
    # Bonus, G, G.1, Type
    # print(len(round))
    # print(round[thing])
    # print(round['Tm'], round['OvPck'], round['Signed'], round['Name'], round['Pos'])


    # draft using statsapi
    # draft = statsapi.get('draft', {'year': 2014})
    # # print(draft['drafts']['draftYear'])
    # for round in draft['drafts']['rounds']:
    #         if round['round'] == '1':
    #             for pick in round['picks']:
    #                 print(pick)
    #                 statsapi.lookup_player()
    #                 print(statsapi.player_stat_data(pick['bisPlayerId']))
    #                 # print(statsapi.get('people', {'personIds': pick['bisPlayerId']}))
    #                 # print(pick)


if __name__ == '__main__':
    main()