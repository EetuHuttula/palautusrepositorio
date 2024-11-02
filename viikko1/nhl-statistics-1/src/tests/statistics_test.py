import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())
        
    def test_search_unknown_player_returns_none(self):
        result = self.stats.search("unknown")
        self.assertIsNone(result)

    def test_search_known_player_returns_correct_player(self):
        result = self.stats.search("Semenko")
        self.assertIsNotNone(result)
        self.assertEqual("Semenko", result.name)

    def test_team_returns_correct_number_of_players(self):
        team_players = self.stats.team("EDM")
        self.assertEqual(3, len(team_players))

    def test_top_returns_player_with_highest_goals(self):
        top_player = self.stats.top(1)[0]
        self.assertEqual(35, top_player.goals)

    def test_top_sorted_by_points(self):
        top_player = self.stats.top(1, SortBy.POINTS)[0]
        self.assertEqual(35, top_player.goals)

    def test_top_sorted_by_goals(self):
        top_player = self.stats.top(1, SortBy.GOALS)[0]
        self.assertEqual(45, top_player.goals)

    def test_top_sorted_by_assists(self):
        top_player = self.stats.top(1, SortBy.ASSISTS)[0]
        self.assertEqual(89, top_player.assists)