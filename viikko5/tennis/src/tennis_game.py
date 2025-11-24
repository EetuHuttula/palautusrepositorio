class TennisGame:
    SCORE_NAMES = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}
    
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0
    
    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1
    
    def get_score(self):
        if self.player1_score == self.player2_score:
            if self.player1_score >= 3:
                return "Deuce"
            return f"{self.SCORE_NAMES[self.player1_score]}-All"

        if self.player1_score >= 4 or self.player2_score >= 4:
            score_diff = self.player1_score - self.player2_score
            if score_diff == 1:
                return "Advantage player1"
            elif score_diff == -1:
                return "Advantage player2"
            elif score_diff >= 2:
                return "Win for player1"
            else:
                return "Win for player2"
        

        return f"{self.SCORE_NAMES[self.player1_score]}-{self.SCORE_NAMES[self.player2_score]}"