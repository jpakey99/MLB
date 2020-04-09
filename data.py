from matplotlib import pyplot as plt
def read_team_csv():
    info = [0] * 92
    file = open("Total_Team_Stats.csv", "r")

    file.readline()
    line_num = 0
    for line in file:
        line = line.strip("\n")
        values = line.split(",")
        info[line_num] = [float(i) for i in values]
        line_num += 1

    file.close()
    return info


def create_table(x_axis, y_axis, title, x_label, y_label, average):
    plt.plot(average[0], average[1] )
    plt.scatter(x_axis, y_axis)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig('I did something.png')
    plt.show()


def main():
    info = read_team_csv()
    x_axis = [0] * (len(info) - 2)
    y_axis = [0] * (len(info) - 2)
    line = 0
    for team in info:
        if line == 0:
            average = [team[3], team[0]]
        elif line <= len(info) - 2 and line > 0:
            y_axis[(line-1)] = team[0]
            x_axis[(line-1)] = team[3]
        line = line + 1
    create_table(x_axis, y_axis, "Win % vs Walks", "Walks", "Win %", average)


main()