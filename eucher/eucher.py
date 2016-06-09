from objects import card
from eucher import euc_cards as e_card
from objects import player as p
from eucher import game_logic as gl
"""
main game for eucher
"""


class EucherPlayer(p.Player):
    """
    creates player object with attributes unique to Eucher
    """

    def __init__(self, player_number):
        super().__init__(player_number)

        self.dealer = False
        self.tricks = 0
        self.card_played = None
        self.team = None
        self.took_last_trick = False


class Eucher(object):
    """
    set up for Eucher game
    """

    def __init__(self, deck):
        self.game = None
        self.deck = deck
        self.HAND_SIZE = 5
        self.NUMBER_OF_PLAYERS = 4
        self.NUMBER_OF_TEAMS = 2
        self.number_of_rounds = 0

    def create_eucher_deck(self):
        for card in self.deck.List:
            if card.RANKS[card.rank] < 9:
                self.deck.List.remove(card)

    # DEBUG METHOD
    def print_cards(self):
        for cards in self.deck.List:
            print(cards.name)

    def create_players(self):
        for player_number in range(self.NUMBER_OF_PLAYERS):
            EucherPlayer(player_number + 1)

    def create_hands(self):
        hand = []

        for slot in range(self.HAND_SIZE):
            card.Deck.shuffle()
            top = card.Deck.List[0]
            # places top card in to hand and removes it from the deck
            card.Deck.List.remove(top)
            hand.append(top)

        return hand

    def deal_hands(self):
        for player in p.Player.List:
            player.hand = self.create_hands()

    def create_teams(self):
        for team_number in range(self.NUMBER_OF_TEAMS):
            p.Team(team_number + 1)

    def team_setup(self):
        self.create_players()
        self.create_teams()

        for player in p.Player.List:
            if (player.player_number - 1) % 4 == 0 or (player.player_number - 1) % 4 == 2:
                player.team = p.Team.List[0]
            else:
                player.team = p.Team.List[1]

    def setup(self):  # initial setup of game
        self.create_eucher_deck()
        self.team_setup()

    @staticmethod
    def game_start():
        game_eucher = Eucher(e_card.EucherDeck())
        game_eucher.setup()
        gl.CallingRound()
        gl.PlayRound()

    def main_game(self):
        gl.CallingRound.calling_round.loop(self.number_of_rounds)
        gl.PlayRound.play_round.loop()
        self.number_of_rounds += 1

