from objects import card


class EucherCard(card.Card):
    """
    sets up attributes for cards in Eucher
    """

    RANKS = {'9': 9, '10': 10, 'Jack': 11,
             'Queen': 12, 'King': 13, 'Ace': 14}

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

        self.trump = False


class Jack(EucherCard):
    """
    creates Jack ranked cards

    in Eucher Jacks are have special attributes when they are made trump
    """

    JACKS = []

    red = []
    black = []

    BOWERS = {'Hearts': 'Diamonds',
              'Diamonds': 'Hearts',
              'Spades': 'Clubs',
              'Clubs': 'Spades'}

    for suit in card.Card.SUITS:
        if suit is 'Hearts' or suit is 'Diamonds':
            red.append(suit)
        else:
            black.append(suit)

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

        self.left_bower = False
        Jack.JACKS.append(self)

    @staticmethod
    def set_left_bower():
        for jack in Jack.JACKS:
            if jack.trump is True:
                for bower in Jack.JACKS:
                    if jack.suit is 'Hearts' and bower.suit is 'Diamonds':
                        bower.left_bower = True
                    elif jack.suit is 'Diamonds' and bower.suit is 'Hearts':
                        bower.left_bower = True
                    elif jack.suit is 'Spades' and bower.suit is 'Clubs':
                        bower.left_bower = True
                    elif jack.suit is 'Clubs' and bower.suit is 'Spades':
                        bower.left_bower = True
        Jack.change_left_bower()

    def change_left_bower(self):  # sets stats for left bower
        if self.left_bower is True:
            for suit in self.BOWERS:
                if self.suit == suit:
                    self.suit = suit



class EucherDeck(card.Deck):
    """
    sets up attributes for deck in Eucher
    """

    ALL_CARDS = []  # I needed a list that had a reference to all the cards in the game for making them trump

    def __init__(self):
        EucherDeck.create_eucher_cards()
        EucherDeck.remove_cards()

    @staticmethod
    def create_eucher_cards():
        for suit in card.Card.SUITS:
            for rank in EucherCard.RANKS:
                if rank == 'Jack':
                    eucher_card = Jack(suit, rank)
                else:
                    eucher_card = EucherCard(suit, rank)
                card.Deck.List.append(eucher_card)
                EucherDeck.ALL_CARDS.append(eucher_card)


    @staticmethod
    def remove_cards():
        for euc_card in card.Deck.List:
            if euc_card.RANKS[euc_card.rank] < 9:
                card.Deck.List.remove(euc_card)