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


class Graph2DScatter:
    def __init__(self, x, y, labels, axis_labels, average_lines=True, inverty=False, invertx=False, size=(23, 10.4), diag_lines=True):
        self.x = x
        self.y = y
        self.labels = labels
        self.average_lines = average_lines
        self.axis_labels = axis_labels
        self.inverty = inverty
        self.invertx = invertx
        self.size = size
        self.diag_lines = diag_lines

    def graph(self):
        fig = plt.figure(figsize=self.size)
        ax = fig.add_subplot()
        # ax.scatter(self.x, self.y)
        for index in range(0,len(self.x)):
            image = OffsetImage(plt.imread(self.labels[index]), zoom=.13)
            ax.autoscale()
            ab = AnnotationBbox(image, (self.x[index], self.y[index]), frameon=False)
            ax.add_artist(ab)
        ax.set_xlabel(self.axis_labels[0], fontsize=18)
        ax.set_ylabel(self.axis_labels[1], fontsize=18)
        if self.average_lines:
            y_mean = [np.mean(self.y)] * len(self.y)
            x_mean = [np.mean(self.x)] * len(self.x)
            ax.plot(self.x, y_mean, label='Mean', color='red')
            ax.plot(x_mean, self.y, label='Mean', color='red')
        if self.diag_lines:
            x_sdev = stdev(self.x)
            y_sdev = stdev(self.y)
            y_list, x_list = [], []
            for value in range(min(self.y), max(self.y), int(y_sdev)):
                y_list.append(value)
            y_list.append(y_list[-1] + y_sdev)
            for value in range(int(min(self.x)), int(max((self.x))), int(x_sdev)):
                x_list.append(value)
            x_list.append(x_list[-1] + x_sdev)
            slope = (max(y_list) - min(y_list)) / (max(x_list) - min(x_list))
            std = -3
            for i in range(0, len(x_list)):
                xl, yl, x, y = [], [], [], []
                for j in range(0, len(y_list)):
                    # shift lines
                    if min(self.x) - (x_sdev / 2) <= x_list[j] + (x_sdev * std) <= max(self.x) + (x_sdev / 2):
                        xl.append(x_list[j] + (x_sdev * std))
                        yl.append(y_list[j])
                std += 1
                ax.plot(xl, yl, label='Mean', color='gray')
        if self.inverty:
            plt.gca().invert_yaxis()
        if self.invertx:
            plt.gca().invert_xaxis()
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
