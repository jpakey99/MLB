yellow, red, brown, blue, green, purple, orange, black = (1,1,0), (1,0,0), (.545,.27,.074), (0,0,1), (0,1,0), (1,0,1), (1,.55,0), (0,0,0)


class MLBLabel:
    def __init__(self):
        self.logos = {
            'mlb': 'logos/_MLB_logo.png',
            'LAA': 'logos/angels.png',
            'HOU': 'logos/astros.png',
            'OAK': 'logos/athletics.png',
            'TOR': 'logos/blueJays.png',
            'ATL': 'logos/braves.png',
            'MIL': 'logos/brewers.png',
            'STL': 'logos/cardinals.png',
            'CHC': 'logos/cubs.png',
            'ARI': 'logos/diamondbacks.png',
            'LAD': 'logos/dodgers.png',
            'SFG': 'logos/giants.png',
            'CLE': 'logos/indians.png',
            'SEA': 'logos/mariners.png',
            'MIA': 'logos/marlins.png',
            'NYM': 'logos/mets.png',
            'WSN': 'logos/nationals.png',
            'BAL': 'logos/orioles.png',
            'SDP': 'logos/padres.png',
            'PHI': 'logos/phillies.png',
            'PIT': 'logos/pirates.png',
            'TEX': 'logos/rangers.png',
            'TBR': 'logos/rays.png',
            'CIN': 'logos/reds.png',
            'BOS': 'logos/redSox.png',
            'COL': 'logos/rockies.png',
            'KCR': 'logos/royals.png',
            'DET': 'logos/tigers.png',
            'MIN': 'logos/twins.png',
            'CHW': 'logos/whiteSox.png',
            'NYY': 'logos/yankees.png'
        }
        self.colors = {
            'mlb': blue,
            'LAA': red,
            'HOU': orange,
            'OAK': green,
            'TOR': blue,
            'ATL': red,
            'MIL': blue,
            'STL': red,
            'CHC': blue,
            'ARI': red,
            'LAD': blue,
            'SFG': orange,
            'CLE': red,
            'SEA': blue,
            'MIA': orange,
            'NYM': orange,
            'WSN': red,
            'BAL': orange,
            'SDP': brown,
            'PHI': red,
            'PIT': yellow,
            'TEX': blue,
            'TBR': blue,
            'CIN': red,
            'BOS': red,
            'COL': purple,
            'KCR': blue,
            'DET': blue,
            'MIN': red,
            'CHW': black,
            'NYY': blue
        }

    def get_labels(self, data):
        labels = []
        for line in data:
            labels.append(self.logos[line])
        return labels

    def get_colors(self, data):
        labels = []
        for line in data:
            labels.append(self.colors[line])
        return labels