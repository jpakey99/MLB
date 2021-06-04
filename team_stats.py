class TeamStats:
    def __init__(self, data):
        self.data = data

    def organize_data(self, team, stat):
        team_list, data_list, combined_list = [], [], []
        for t in team:
            team_list.append(t)
        for w in stat:
            data_list.append(w)
        for i in range(0, len(team_list)):
            combined_list.append((team_list[i], data_list[i]))
        return combined_list

    def get_data(self, key):
        team = self.data['Team']
        stat = self.data[key]
        return self.organize_data(team, stat)

