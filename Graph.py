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
            ymid = (ax.get_ylim()[0] + ax.get_ylim()[1])/2
            xmid = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
            ysteps = (ax.get_ylim()[1] - ax.get_ylim()[0])//(y_sdev/2)
            xsteps = (ax.get_xlim()[1] - ax.get_xlim()[0]) // (x_sdev)
            print(int(0-(ysteps/2)), int(0+(ysteps/2)))
            for i in range(int(0-(ysteps/2)), int(0+(ysteps/2))):
                y_list.append(ymid + (i*y_sdev))
            for i in range(int(0-(xsteps/2)), int(0+(xsteps/2))):
                x_list.append(xmid + (i * x_sdev))
            x_list.append(x_list[-1] + x_sdev)
            slope = (y_list[0] - y_list[-1]) / (min(x_list) - max(x_list))
            for pointx in x_list:
                # plt.scatter(x=pointx, y=ymid, color='blue')
                plt.axline((pointx, ymid), slope=slope, color='gray')
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
