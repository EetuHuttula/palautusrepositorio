import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    def test_search_finds_player(self):
        player = self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 37)
        self.assertEqual(player.assists, 53)

    def test_search_returns_none_if_player_not_found(self):
        player = self.stats.search("NonExistent")
        self.assertIsNone(player)

    def test_team_returns_correct_players(self):
        edmonton_players = self.stats.team("EDM")
        self.assertEqual(len(edmonton_players), 3)
        
        player_names = set(player.name for player in edmonton_players)
        self.assertEqual(player_names, {"Semenko", "Kurri", "Gretzky"})

    def test_team_returns_empty_list_if_team_not_found(self):
        team_players = self.stats.team("NONEXISTENT")
        self.assertEqual(len(team_players), 0)

    def test_top_returns_correct_number_of_players(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 4) 

    def test_top_returns_players_by_points_by_default(self):
        top_players = self.stats.top(3)
        # Järjestys pisteiden mukaan
        self.assertEqual(top_players[0].name, "Gretzky")   
        self.assertEqual(top_players[1].name, "Lemieux")   
        self.assertEqual(top_players[2].name, "Yzerman")  
        self.assertEqual(top_players[3].name, "Kurri")     

    def test_top_returns_players_by_goals(self):
        top_players = self.stats.top(3, SortBy.GOALS)
        # Järjestys maalien mukaan
        self.assertEqual(top_players[0].name, "Lemieux")   # 45 maalia
        self.assertEqual(top_players[1].name, "Yzerman")   # 42 maalia
        self.assertEqual(top_players[2].name, "Kurri")     # 37 maalia
        self.assertEqual(top_players[3].name, "Gretzky")   # 35 maalia

    def test_top_returns_players_by_assists(self):
        top_players = self.stats.top(3, SortBy.ASSISTS)
        # Järjestys syöttöjen mukaan
        self.assertEqual(top_players[0].name, "Gretzky")   # 89 syöttöä
        self.assertEqual(top_players[1].name, "Yzerman")   # 56 syöttöä
        self.assertEqual(top_players[2].name, "Lemieux")   # 54 syöttöä
        self.assertEqual(top_players[3].name, "Kurri")     # 53 syöttöä