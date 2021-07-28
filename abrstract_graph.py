from PIL import Image, ImageDraw, ImageFont
from labels import MLBLabel


class AbstractGraph:
    def __init__(self, title, credits, subtitle, date):
        self.title = title
        self.credits = credits
        self.subtitle = subtitle
        self.date = date
        self.width, self.height = 1920, 1028
        self.labels = MLBLabel()
        self.image = Image.new('RGBA', (self.width, self.height))
        self.draw = ImageDraw.ImageDraw(self.image)
        self.draw.rectangle((0, 0, self.width, self.height), fill=(255, 255, 255, 255))
        self.title_font = ImageFont.truetype('Roboto-Regular.ttf', 50)
        self.sub_title_font = ImageFont.truetype('Roboto-Regular.ttf', 30)

    def save_image(self):
        self.image.save('graphs//' + self.title + '_' + self.date + '.png')


class ScatterGraph(AbstractGraph):
    def __init__(self, title, credits, subtitle,date, corner_labels):
        super().__init__(title, credits, subtitle, date)
        self.corner_labels = corner_labels

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
        self.draw.text(((text_box), (self.height / 2) - th), text=self.title, fill=(0, 0, 0, 255), font=self.title_font)
        self.draw.text(((text_box), (self.height / 2) + (sh)), text=self.subtitle, fill=(0, 0, 0, 255), font=self.sub_title_font)
        self.draw.text(((text_box), (self.height / 2) + (2 * ch)), text=self.credits, fill=(0, 0, 0, 255), font=self.sub_title_font)

    def create_image(self):
        x, y = 800, 20
        self.title_placement()
        self.graph.graph().savefig('1', bbox_inches='tight')
        g: Image.Image = Image.open('1.png')
        self.graph_size = g.size
        self.image.paste(g, box=(x, y))
        self.corner_label_placement()