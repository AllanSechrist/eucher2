import random

class Card(object):

    RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11,
             'Queen': 12, 'King': 13, 'Ace': 14}

    SUITS = ['Hearts', 'Diamonds', 'Spades', 'Clubs']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = (self.rank + ' of ' + self.suit)


class Deck(object):
    """
    creates a deck object
    """

    List = []

    def __init__(self):
        Deck.create_cards(Card)

    @staticmethod
    def create_cards(card):
        for suit in card.SUITS:
            for rank in card.RANKS.keys():
                Deck.List.append(card(suit, rank))

    @staticmethod
    def shuffle():
        random.shuffle(Deck.List)

