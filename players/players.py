import pybaseball
import team_stats

'''
Every Player Stat item needs: Name, Team, Position, Age, Stat_Value
'''


def organize_data(team, name, age, stat):
    print(len(team), len(name), len(age), len(stat))
    team_list, data_list, combined_list, name_list, age_list, pos_list = [], [], [], [], [], []
    for t in team:
        team_list.append(t)
    for s in stat:
        data_list.append(s)
    for n in name:
        name_list.append(n)
    # for p in position:
    #     data_list.append(p)
    for a in age:
        age_list.append(a)
    # print(len(team_list), len(name_list), len(age_list), len(data_list))
    for i in range(0, len(team_list)-1):
        n = name_list[i]
        t = team_list[i]
        a = age_list[i]
        d = data_list[i]
        combined_list.append((name_list[i], team_list[i], age_list[i], data_list[i]))
    return combined_list


class PlayerStats:
    def __init__(self, data):
        self.data = data

    def get_data(self, key):
        name = self.data['Name']
        # print(name)
        team = self.data['Team']
        age = self.data['Age']
        # pos = self.data['Pos']
        # print('pos')
        # print(pos)
        stat = self.data[key]
        return organize_data(team, name, age, stat)


class PlayerBattingStats(PlayerStats):
    def __init__(self, year):
        super().__init__(pybaseball.batting_leaders.fg_batting_data(start_season=year))

    def get_xwOBA(self):
        return self.get_data('xwOBA')

    def get_hard_hit(self):
        return self.get_data('HardHit%')


# batters = pybaseball.batting_leaders.fg_batting_data(start_season=2021)

# for i in batters:
#     print(i)

pbs = PlayerBattingStats(2021)
wba = pbs.get_xwOBA()
hh = pbs.get_hard_hit()
print(len(wba), len(hh))