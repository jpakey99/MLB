import numpy as np
from statistics import stdev
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
# read from a file
# get mean, std deviation for entire league
# calculate z-scores for entire league
# plot z-scores on histogram
# For graphs:
# 1: shows all players on a graph
# 2: Select to only show a certain team and add player name to bottom
from matplotlib import colors


def read_file(file_name):
    file = open(file_name)
    file.readline()
    prospects = []
    for line in file:
        split_line = line.split(',')
        # Season,Name,Team,Level,Age,G,PA,AVG,BB%,K%,ISO,BABIP,wRAA,wOBA,wRC+,LD%,GB%,FB%,Pull%,Cent%,Oppo%,SwStr%,Pitches,PlayerId
        prospects.append(split_line)
    return prospects


def get_statistics(data):
    mean = np.mean(data)
    std = stdev(data)
    return mean, std


def find_z_score(mean, value):
    top = value - mean
    bottom = stdev(data)
    return top / bottom


def plot_histogram(data):
    fig = plt.figure(figsize=(12.2,12))
    ax = fig.add_subplot()
    n_bins = 15

    x = data
    N, bins, patches = ax.hist(x, bins=n_bins)
    # Generate a normal distribution, center at x=0 and y=5
    # we need to normalize the data to 0..1 for the full range of the colormap
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    # We can set the number of bins with the `bins` kwarg
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    fig.show()


if __name__ == '__main__':
    prospects = read_file('AAA_East.csv')
    data = []
    for prospect in prospects:
        data.append(float(prospect[12]))
    mean, std = get_statistics(data)
    z_scores = []
    for datum in data:
        z_scores.append(find_z_score(mean, datum))
    print(z_scores)
    fig = plot_histogram(z_scores)