from tennis_game import TennisGame
# This is a simple demonstration of the TennisGame class functionality.

def main():
    game = TennisGame("player1", "player2")

    print(game.get_score())

    game.won_point("player1")
    print(game.get_score())

    game.won_point("player1")
    print(game.get_score())

    game.won_point("player2")
    print(game.get_score())

    game.won_point("player1")
    print(game.get_score())

    game.won_point("player1")
    print(game.get_score())


if __name__ == "__main__":
    main()
