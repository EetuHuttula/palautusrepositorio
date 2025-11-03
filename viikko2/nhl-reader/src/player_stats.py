class PlayerStats:
    def __init__(self, players):
        self.players = players

    def top_scorers_by_nationality(self, nationality):
        filtered = []
        for player in self.players:
            if player.nationality == nationality:
                filtered.append(player)

        sorted_players = sorted(filtered, key=lambda p: p.points(), reverse=True)
        return sorted_players
