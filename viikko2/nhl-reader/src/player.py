class Player:
    def __init__(self, player_reader_dict):
        self.name = player_reader_dict['name']
        self.team= player_reader_dict["team"]
        self.goals = player_reader_dict["goals"]
        self.assists = player_reader_dict["assists"]
        self.nationality = player_reader_dict["nationality"]

    def points(self):
        return self.goals + self.assists
    def __str__(self):
        return f"{self.name:20} {self.team:5} {self.goals:2} + {self.assists:2} = {self.points()}"
