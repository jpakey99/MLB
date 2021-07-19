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
        self.id_logos = {
            108 : 'logos/angels.png',
            117 : 'logos/astros.png',
            133 : 'logos/athletics.png',
            141 : 'logos/blueJays.png',
            144 : 'logos/braves.png',
            158 : 'logos/brewers.png',
            138 : 'logos/cardinals.png',
            112 : 'logos/cubs.png',
            109 : 'logos/diamondbacks.png',
            119 : 'logos/dodgers.png',
            137 : 'logos/giants.png',
            114 : 'logos/indians.png',
            136 : 'logos/mariners.png',
            146 : 'logos/marlins.png',
            121 : 'logos/mets.png',
            120 : 'logos/nationals.png',
            110 : 'logos/orioles.png',
            135 : 'logos/padres.png',
            143 : 'logos/phillies.png',
            134 : 'logos/pirates.png',
            140 : 'logos/rangers.png',
            139 : 'logos/rays.png',
            113 : 'logos/reds.png',
            111 : 'logos/redSox.png',
            115 : 'logos/rockies.png',
            118 : 'logos/royals.png',
            116 : 'logos/tigers.png',
            142 : 'logos/twins.png',
            145: 'logos/whiteSox.png',
            147 : 'logos/yankees.png'
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
        self.abbr = {
            'LAA': 'Los Angeles Angels',
            'HOU': 'Houston Astros',
            'OAK': 'Oakland Athletics',
            'TOR': 'Toronto Blue Jays',
            'ATL': 'Atlanta Braves',
            'MIL': 'Milwaukee Brewers',
            'STL': 'St. Louis Cardinals',
            'CHC': 'Chicago Cubs',
            'ARI': 'Arizona Diamondbacks',
            'LAD': 'Los Angeles Dodgers',
            'SFG': 'San Francisco Giants',
            'CLE': 'Cleveland Indians',
            'SEA': 'Seattle Mariners',
            'MIA': 'Miami Marlins',
            'NYM': 'New York Mets',
            'WSN': 'Washington Nationals',
            'BAL': 'Baltimore Orioles',
            'SDP': 'San Diego Padres',
            'PHI': 'Philadelphia Phillies',
            'PIT': 'Pittsburgh Pirates',
            'TEX': 'Texas Rangers',
            'TBR': 'Tampa Bay Rays',
            'CIN': 'Cincinnati Reds',
            'BOS': 'Boston Red Sox',
            'COL': 'Colorado Rockies',
            'KCR': 'Kansas City Royals',
            'DET': 'Detroit Tigers',
            'MIN': 'Minnesota Twins',
            'CHW': 'Chicago White Sox',
            'NYY': 'New York Yankees'
        }

    def get_labels(self, data):
        labels = []
        for line in data:
            labels.append(self.logos[line])
        return labels

    def get_labels_by_id(self, data):
        labels = []
        for line in data:
            labels.append(self.id_logos[line])
        return labels

    def get_colors(self, data):
        labels = []
        for line in data:
            labels.append(self.colors[line])
        return labels