import requests
from player import Player

class PlayerReader:
    def __init__(self, season):
        self.season = season
        self.base_url = "https://studies.cs.helsinki.fi/nhlstats"

    def get_players(self):
        url = f"{self.base_url}/{self.season}/players"
        response = requests.get(url).json()
        players = []
        for player_dict in response:
            players.append(Player(player_dict))
        return players
