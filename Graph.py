import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from statistics import stdev

# bar graph
# pie graph
params = {'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
pylab.rcParams.update(params)


class Modifier:
    def add_modification(self):
        pass


class AverageLines(Modifier):
    def __init__(self, ax, average, x, y):
        self.ax = ax
        self.x = x
        self.y = y
        if average == (None, None):
            self.y_mean = [np.mean(self.y)] * len(self.y)
            self.x_mean = [np.mean(self.x)] * len(self.x)
        else:
            self.y_mean = [(average[1])] * len(self.y)
            self.x_mean = [(average[0])] * len(self.x)

    def add_modification(self):
        self.ax.plot(self.x, self.y_mean, label='Mean', color='red')
        self.ax.plot(self.x_mean, self.y, label='Mean', color='red')


class InvertY(Modifier):
    def __init__(self):
        pass

    def add_modification(self):
        plt.gca().invert_yaxis()


class InvertX(Modifier):
    def __init__(self):
        pass

    def add_modification(self):
        plt.gca().invert_xaxis()


class DiagonalLines(Modifier):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.x = x
        self.y = y

    def add_modification(self):
        x_sdev = stdev(self.x)
        y_sdev = stdev(self.y)
        y_list, x_list = [], []
        ymid = (self.ax.get_ylim()[0] + self.ax.get_ylim()[1]) / 2
        xmid = (self.ax.get_xlim()[0] + self.ax.get_xlim()[1]) / 2
        ysteps = abs((self.ax.get_ylim()[1] - self.ax.get_ylim()[0]) // (y_sdev / 2))
        xsteps = abs((self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) // (x_sdev))
        print(int(0 - (ysteps / 2)), int(0 + (ysteps / 2)))
        for i in range(int(0 - (ysteps / 2)), int(0 + (ysteps / 2))):
            y_list.append(ymid + (i * y_sdev))
        for i in range(int(0 - (xsteps / 2)), int(0 + (xsteps / 2))):
            x_list.append(xmid + (i * x_sdev))
        x_list.append(x_list[-1] + x_sdev)
        print(y_list)
        slope = (y_list[0] - y_list[-1]) / (min(x_list) - max(x_list))
        for pointx in x_list:
            # plt.scatter(x=pointx, y=ymid, color='blue')
            plt.axline((pointx, ymid), slope=slope, color='gray')


class BestFit(Modifier):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_modification(self):
        plt.plot(np.unique(self.x), np.poly1d(np.polyfit(self.x, self.y, 1))(np.unique(self.x)), color='green')


class PointLabels(Modifier):
    def __init__(self, ax, x, y, labels):
        self.ax = ax
        self.x = x
        self.y = y
        self.labels = labels

    def add_modification(self):
        for index in range(0, len(self.x)):
            self.ax.annotate(self.labels[index], (self.x[index], self.y[index]), textcoords="offset points", ha='center', xytext=(0, -25))


class Graph2DScatter:
    def __init__(self, x, y, labels, axis_labels, average_lines=True, inverty=False, invertx=False, size=(12.2,12), diag_lines=True, best_fit=False, dot_labels=None, average=(None, None)):
        self.modifiers = []
        self.x = x
        self.y = y
        self.labels = labels
        self.fig = plt.figure(figsize=size)
        self.ax = self.fig.add_subplot()
        if dot_labels is None:
            self.dot_labels = []
        else:
            self.modifiers.append(PointLabels(self.ax, self.x, self.y, dot_labels))
        if average_lines:
            self.modifiers.append(AverageLines(self.ax, average, x=self.x, y=self.y))
        self.axis_labels = axis_labels
        if inverty:
            self.modifiers.append(InvertY())
        if invertx:
            self.modifiers.append(InvertX())
        if diag_lines:
            self.modifiers.append(DiagonalLines(self.ax, self.x, self.y))
        if best_fit:
            self.modifiers.append(BestFit(self.x, self.y))

    def graph(self):
        # ax.scatter(self.x, self.y)
        for index in range(0,len(self.x)):
            image = OffsetImage(plt.imread(self.labels[index]), zoom=.13)
            self.ax.autoscale()
            ab = AnnotationBbox(image, (self.x[index], self.y[index]), frameon=False)
            self.ax.add_artist(ab)
        self.ax.set_xlabel(self.axis_labels[0], fontsize=18)
        self.ax.set_ylabel(self.axis_labels[1], fontsize=18)
        for modifier in self.modifiers:
            modifier.add_modification()
        return plt


class BarGraph:
    def __init__(self, x, y, title, y_label='Run Diff', labels=None, colors=None, credit=True, x_ticks=False):
        self.x = x
        self.y = y
        self.title = title
        self.labels = labels
        self.colors = colors
        self.credit = credit
        self.x_ticks = x_ticks
        self.y_label = y_label
        params = {'xtick.labelsize': 'x-large',
                  'ytick.labelsize': 'x-large'}
        pylab.rcParams.update(params)

    def graph(self):
        fig = plt.figure(figsize=(23, 10.7))
        ax = fig.add_subplot()
        if self.colors is None:
            print(self.x, self.y)
            plt.bar(self.x, self.y)
        else:
            plt.bar(self.x, self.y, edgecolor='black', linewidth=2, color=self.colors)
        plt.margins(0.01, 0.01)
        plt.grid(axis='y')
        if not self.x_ticks:
            plt.xticks([])
        if self.labels is not None:
            for index in range(len(self.x)):
                image = OffsetImage(plt.imread(self.labels[index]), zoom=.13)
                ax.autoscale()
                if self.y[index] > 0:
                    ly = -5
                else:
                    ly = 5
                ab = AnnotationBbox(image, (self.x[index], ly), frameon=False)
                ax.add_artist(ab)
        plt.ylabel(self.y_label, fontsize=18)
        return plt


class TeamCardGraph:
    def __init__(self, stats, values, title, credit=False, xaxis=False):
        self.stats = stats
        self.values = values
        self.title = title
        self.credit = credit
        self.xaxis = xaxis
        params = {'xtick.labelsize': 'x-large',
                  'ytick.labelsize': 'x-large'}
        pylab.rcParams.update(params)
        # self.red_scale = [(1,.17,.078), ()]

    def graph(self):
        fig = plt.figure(figsize=(10, 10.7))
        ax = fig.add_subplot()
        axis = plt.gca()
        axis.set_ylim(-3, 3)
        plt.yticks([-3, -2, -1, 0, 1, 2, 3], ['-3', '-2', '-1', '0', '1', '2', '3'])
        plt.grid(axis='y')
        for i in range(0, len(self.stats)):
            r, g, b = 0, 0, 0
            if self.values[i] < 0:
                r = 1
                g = b = 1 - abs(self.values[i] / 3)
            else:
                g = b = 1
                r = 1 - abs(self.values[i] / 3)
            plt.bar(self.stats[i], self.values[i], edgecolor='black', linewidth=2, color=(r, g, b))
        plt.ylabel('z-score', fontsize=18)
        return plt
