from objects import card


class Eucher_Card(card.Card):
    """
    sets up attributes for cards in Eucher
    """

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

        self.trump = False


class Eucher_Deck(card.Deck):
    """
    sets up attributes for deck in Eucher
    """

    def __init__(self):
        Eucher_Deck.create_cards(Eucher_Card)