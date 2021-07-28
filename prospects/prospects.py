import numpy as np
from statistics import stdev
import matplotlib, statistics
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import scipy.stats as stats
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


def normaldist(mean, std, value):
    return stats.norm.cdf((value-mean)/std)


if __name__ == '__main__':
    prospects = read_file('AAA_East.csv')
    data, age = [], []
    for prospect in prospects:
        data.append(float(prospect[12]))
        age.append(int(prospect[4]))
    mean, std = get_statistics(data)
    age_mean, age_std = get_statistics(age)
    z_scores, age_z_scores = [], []
    for datum in data:
        z_scores.append(find_z_score(mean, datum))
    for datum in age:
        age_z_scores.append(find_z_score(age_mean, datum))
    z_mean, z_std = get_statistics(z_scores)
    age_z_mean, age_z_std = get_statistics(age_z_scores)
    print(z_scores)
    # fig = plot_histogram(z_scores)
    normal_values = []
    for z in z_scores:
        normal_values.append(normaldist(z_mean, z_std, z))
    n_mean, n_std = get_statistics(normal_values)
    for i, n in enumerate(normal_values):
        x = (n - n_mean) / n_std
        value = (round(x, 1)*3)
        scout = 50 + (5 * value)
        print(scout, prospects[i][1])