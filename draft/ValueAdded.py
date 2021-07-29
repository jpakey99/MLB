from Graph import BarGraph
import csv
from labels import MLBLabel
from PIL import Image, ImageDraw, ImageFont


def read_file():
    with open('draft/rankings/2021_draft.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        PICK_TEAM, NAME, FV = 2, 3, 13
        picks = []
        for row in spamreader:
            print(row)
            if spamreader.line_num != 1:
                if '-' in row[PICK_TEAM] or row[PICK_TEAM] == '':
                    pick_num = -1
                    team = 'mlb'
                else:
                    pick_team = row[PICK_TEAM].split('/')
                    pick_num = int(pick_team[0].strip('"'))
                    team = pick_team[1].strip('"')
                if row[FV] == '':
                    fv = 20
                else:
                    fv = int(row[FV].strip('+').strip('"'))
                name = row[NAME].strip('"')
                pick = (pick_num, team, name, fv)
                picks.append(pick)
    return picks


def convert_to_war(fv):
    war = {
        20: -2.0,
        30: -.1,
        35: 0.0,
        40: .7,
        45: 1.5,
        50: 2.4,
        55: 3.3,
        60: 4.9,
        70: 7.0,
        80: 8.0
    }
    return war[fv]


def assign_value(data):
    team_dict = {}
    for datum in data:
        fv = convert_to_war(datum[3])
        if datum[1] not in ['mlb', '']:
            if datum[1] in team_dict.keys():
                team_dict[datum[1]] += fv
            else:
                team_dict[datum[1]] = fv
    return team_dict


class ValueAdded:
    def __init__(self):
        self.title = 'Combined WAR Value at time of Draft'
        self.credits = 'Data: @fangraphs'
        self.subtitle = '2021 MLB Draft'
        self.date = '2019'
        self.width, self.height = 1920, 1028
        self.image = Image.new('RGBA', (self.width, self.height))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, self.width, self.height), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        data = read_file()
        values = assign_value(data)
        print(values)
        self.combined = []
        for key in values.keys():
            self.combined.append((key.upper(), values[key]))
        teams, values = self.sort()
        print(self.combined)
        colors = MLBLabel().get_colors(teams)
        self.graph = BarGraph(teams, values, 'Value Added', x_ticks=True, colors=colors, y_label='Projected WAR at Time of Draft')

    def create_image(self):
        y = 160
        tw,th = self.draw.textsize(self.title, font=self.title_font)
        sw, th = self.draw.textsize(self.subtitle, font=self.sub_title_font)
        cw, th = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((self.width - tw)/2, 10), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((self.width - sw)/2, 70), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((self.width - cw)/2, 100), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.graph.graph().savefig('1', bbox_inches='tight')
        self.image.paste(Image.open('1.png'), box=(20, y))

    def save_image(self):
        self.image.save('draft//' + 'DraftValueAdded' + '_' + self.date + '.png')

    def sort(self):
        for i in range(0, len(self.combined)):
            for j in range(0, len(self.combined)-1):
                if self.combined[j][1] < self.combined[j+1][1]:
                    temp = self.combined[j]
                    # print(temp)
                    self.combined[j] = self.combined[j + 1]
                    self.combined[j + 1] = temp
        teams, values, colors = [], [], []
        for value in self.combined:
            teams.append(value[0])
            values.append(value[1])
        return teams, values
