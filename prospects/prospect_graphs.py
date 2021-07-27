from prospects.prospects import read_file
from labels import MLBLabel
from PIL import Image, ImageDraw, ImageFont
from labels import MLBLabel
from Graph import *
WIDTH, HEIGHT = 1920,1028


class ProspectGraph:
    def __init__(self,x, y, date: str):
        self.date = date
        # self.year = int(date.split('-')[2])
        self.labels = MLBLabel()
        self.image = Image.new('RGBA', (WIDTH, HEIGHT))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        self.x = x
        self.y = y

    def corner_label_placement(self):
        x, y = 800, 20
        gx, gy = self.graph_size
        right_edge = x+ gx - 20
        left_edge = x + 110
        bottom_egge = y+gy-80
        top_edge = y - 20
        trw, trh = self.draw.textsize(self.corner_labels[0], font=self.sub_title_font)
        brw, brh = self.draw.textsize(self.corner_labels[3], font=self.sub_title_font)
        self.draw.text((left_edge, top_edge + trh), text=self.corner_labels[1], fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((left_edge, bottom_egge - brh), text=self.corner_labels[3], fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((right_edge - trw, top_edge + trh), text=self.corner_labels[0], fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text((right_edge - brw,bottom_egge - brh), text=self.corner_labels[2], fill=(0, 0, 0, 255), font=self.sub_title_font)

    def title_placement(self):
        x, y = 800, 20
        text_box = 70
        tw, th = self.draw.textsize(self.title, font=self.title_font)
        sw, sh = self.draw.textsize(self.subtitle, font=self.sub_title_font)
        cw, ch = self.draw.textsize(self.credits, font=self.sub_title_font)
        self.draw.text(((text_box), (HEIGHT / 2) - th), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((text_box), (HEIGHT / 2) + (sh)), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((text_box), (HEIGHT / 2) + (2 * ch)), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)

    def create_image(self):
        x, y = 800, 20
        self.title_placement()
        self.graph.graph().savefig('1', bbox_inches='tight')
        g :Image.Image= Image.open('1.png')
        self.graph_size = g.size
        self.image.paste(g, box=(x, y))
        self.corner_label_placement()


class WalkRateVsWRAA(ProspectGraph):
    def __init__(self, date: str):
        prospects = read_file('prospects/AAA_East.csv')
        walk_rate, wRAA, team = [], [], []
        for prospect in prospects:
            walk_rate.append(float(prospect[9]))
            wRAA.append(float(prospect[12]))
            team.append(prospect[2].strip('"'))
        labels = MLBLabel().get_labels(team)
        super().__init__(wRAA, walk_rate, date)
        self.title = 'Walk % Vs wRAA'
        self.corner_labels = ('', '', '', '')
        self.subtitle = '2021 AAA East'
        self.credits = 'Twitter: @jpakey99, Idea: @ShutdownLine\n data: Fangraphs'  #Fine tone centering 2nd line
        self.graph = Graph2DScatter(self.x, self.y,labels=labels, axis_labels=['wRAA', 'Walk%'], average_lines=True, inverty=False, invertx=False, diag_lines=False)

    def save_image(self):
        self.image.save('graphs//' + 'Prosects_WalkVswRAA' + '_' + self.date + '.png')


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
