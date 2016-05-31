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


class Hand(object):
    """
    creates a hand of cards
    """

    def __init__(self, size):
        self.cards = []  # a list to store the cards in this hand
        self.size = size
        self.make_hand()

    def make_hand(self):
        for slot in range(Hand.size):
            self.swap(Deck.List[0])

    def swap(self, card):
        Deck.List.remove(card)
        self.cards.append(card)