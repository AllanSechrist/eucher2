from objects import game
from objects import card
from eucher import eucher

def main():
    game.game_loop(eucher.Eucher(card.Deck.List))

    quit()


if __name__ == "__main__":
    main()