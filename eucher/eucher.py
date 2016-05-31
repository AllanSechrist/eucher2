from objects import card
from eucher import euc_cards as e_card
from objects import player as p
"""
main game for eucher
"""

class Eucher_Player(p.Player):
    """
    creates eucher player
    """

    def __init__(self, player_number):
        super().__init__(player_number)

        self.dealer = False
        self.tricks = 0
        self.card_played = None
        self.team = None


class Eucher(object):
    """
    set up for Eucher game
    """

    def __init__(self, deck):
        self.game = None
        self.deck = deck
        self.hand_size = 5
        self.number_of_players = 4
        self.number_of_teams = 2

    def create_eucher_deck(self):
        for card in self.deck.List:
            if card.RANKS[card.rank] < 9:
                self.deck.List.remove(card)

    # DEBUG METHOD
    def print_cards(self):
        for cards in self.deck.List:
            print(cards.name)

    def create_players(self):
        for player_number in range(self.number_of_players):
            Eucher_Player(player_number + 1)

    def create_teams(self):
        for team_number in range(self.number_of_teams):
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



def game_start():
    game_eucher = Eucher(e_card.Eucher_Deck())
    game_eucher.setup()

# ---------DEBUG
    for player in p.Player.List:
        print('player number: ' + str(player.player_number))
        print('players team number: ' + str(player.team.team_number))

    for team in p.Team.List:
        print(team.team_number)
# ---------END DEBUG