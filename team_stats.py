import pybaseball


def organize_data(team, stat):
    team_list, data_list, combined_list = [], [], []
    for t in team:
        team_list.append(t)
    for w in stat:
        data_list.append(w)
    for i in range(0, len(team_list)):
        combined_list.append((team_list[i], data_list[i]))
    return combined_list


class TeamStats:
    def __init__(self, data):
        self.data = data

    def get_data(self, key):
        team = self.data['Tm']
        stat = self.data[key]
        return organize_data(team, stat)


class TeamStandings(TeamStats):
    def __init__(self, year):
        super().__init__(pybaseball.standings())

    def get_data(self, key):
        data = []
        for division in self.data:
            team = division['Tm']
            stat = division[key]
            org_data = organize_data(team, stat)
            for team in org_data:
                data.append(team)
        return data

    def get_standings(self):
        d = self.get_data('W-L%')
        team_list = []
        for team in d:
            team_list.append(team)
        return team_list

