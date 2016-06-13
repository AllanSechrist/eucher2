"""
game logic goes here
"""

from objects import player as plr
from objects import card as cd
from eucher import euc_cards as ecd
import random


def play_order(list, number):
    play_order = [list[(number - 1) % 4],
                  list[number % 4],
                  list[(number + 1) % 4],
                  list[(number + 2) % 4]]
    return play_order


def assign_deal_order():  # sets up turn order at the start of each round
    player_list = plr.Player.List

    for player in player_list:
        if player.dealer is True:
            return play_order(player_list, player.player_number + 1)


def assign_play_order():  # play order will change after each trick
    player_list = plr.Player.List

    for player in player_list:
        if player.took_last_trick is True:
            player.took_last_trick = False  # ensure that variable is set to False after play order has been set
            return play_order(player_list, player.player_number)



def assign_dealer(count):
    if count < 1:
        dealer = random.choice(plr.Player.List)  # assign random person to be dealer at the game start
        dealer.dealer = True
        print('player ' + str(dealer.player_number) + ' has been made dealer')

        # debug
        print(dealer.dealer)
    else:  # if not the start of the game, the person to the left of the dealer becomes the new dealer
        for player in plr.Player.List:
            if player.dealer is True:
                player.dealer = False
                plr.Player.List[player.player_number % 4].dealer = True


class CallingRound(object):

    """
    manages player interaction for calling trump
    """

    calling_round = None

    def __init__(self):
        # debug
        print(len(cd.Deck.List))
        self.top_card = cd.Deck.List[0]
        self.play_order = []
        CallingRound.calling_round = self

    def loop(self, count):  # manages class methods
        assign_dealer(count)
        self.play_order = assign_deal_order()
        done = False
        while not done:
            print(self.top_card.suit)
            print(self.top_card.name)
            done = self.pass_or_call()

    @staticmethod
    def make_suit_trump(suit):
        for card in ecd.EucherDeck.ALL_CARDS:
            if card.suit is suit:
                card.trump = True
        ecd.Jack.set_left_bower()

        # debug //////////////////////////////////////////////////////
        """
        print()
        for player in plr.Player.List:
            for card in player.hand:
                if card.trump is True:
                    print(card.name)
        for card in cd.Deck.List:
            if card.trump is True:
                print(card.name)
        print()
        for card in ecd.EucherDeck.ALL_CARDS:
            if card.trump is True:
                print(card.name)
        print()
        for card in ecd.Jack.JACKS:
            print(card.name)
        print()
        for suit in ecd.Jack.red:
            print(suit)
        for suit in ecd.Jack.black:
            print(suit)
        """
        # end debug ////////////////////////////////////////////////////

    def pass_or_call(self):
        for player in self.play_order:
            done = False
            while not done:
                player_input = self.get_player_input(player)
                if player_input == 'PASS':
                    done = True
                elif player_input == 'TRUMP':
                    print(self.top_card.suit + ' has been made trump')
                    self.make_suit_trump(self.top_card.suit)
                    self.pick_up_trump()  # deal must pick up the face up card and discard a card(can be they picked up)
                    return True
                else:
                    print('invalid input')

        return self.pass_or_call_2()

    @staticmethod
    def get_player_input(player):
        player_input = input('player ' + str(player.player_number) + ' PASS or TRUMP? :').upper()
        return player_input

    def pick_up_trump(self):
        dealers_hand = self.play_order[3].hand

        dealers_hand.append(self.top_card)  # adds the top card of the kitty ot the dealers hand
        cd.Deck.List.remove(self.top_card)  # removes top card from the kitty

        print()
        for card in dealers_hand:
            print(card.name)
        print()

        done = False
        while not done:
            dealer_input = input('plaese select a card to discard: ').lower()
            for card in dealers_hand:
                if card.name.lower() == dealer_input:
                    dealers_hand.remove(card)  # removes chosen card from dealers hand
                    cd.Deck.List.append(card)  # places chosen card into the kitty
                    done = True

    # condition after all players pass for the first time change

    def pass_or_call_2(self):

        print()
        print('second pass or call')
        print()

        for player in self.play_order:
            done = False
            while not done:
                player_input = self.get_player_input(player)
                if player_input == 'PASS':
                    done = True
                elif player_input == 'TRUMP':
                    while True:
                        trump_input = input('please select a suit to call trump: ')
                        for suit in cd.Card.SUITS:

                            if trump_input == suit and suit != self.top_card.suit:
                                print(suit + ' has been made trump')
                                self.make_suit_trump(trump_input)  # make selected suit trump
                                return True
                            elif trump_input == self.top_card.suit:
                                print('You cannot call that trump')
                                break

                else:
                    print('invalid input')


# --------------- PLAY ROUND LOGIC -----------------

class PlayRound(object):
    """
    manages player interaction
    """

    play_round = None

    def __init__(self):
        self.count = 0
        self.board = []
        PlayRound.play_round = self

    def loop(self):
        done = False

        while not done:

            if self.count == 0:
                play_order = assign_deal_order()
            else:
                play_order = assign_play_order()

            # self.reset_players()

            for player in play_order:
                self.select_card(player)

            # debug ///////////////////////////////////////////
            print()
            for card in self.board:
                print(card.name)
            # end debug ///////////////////////////////////////////

            self.select_highest_card()  # picks highest card and awards the trick to the player who played it
            self.clean_board()

            self.count += 1

            if self.count > 4:
                done = True
                self.award_points()
                self.clear_trump()

                # debug //////////////////////////////////////////////////
                for team in plr.Team.List:
                    print(team.points)
                # end debug

    def select_card(self, player):
        print()
        print('player ' + str(player.player_number) + ' please select a card to play')
        print()
        for card in player.hand:
            print(card.name)

        done = False
        while not done:
            print()
            player_input = input('please select a card to play: ').lower()
            for card in player.hand:
                if card.name.lower() == player_input:
                    done = self.check_suit(card, player)  # check if player is following suit

    def play_card(self, card, player):  # removes selected card from player's hand and adds it to the board

        self.board.append(card)
        player.hand.remove(card)
        player.card_played = card

    def check_suit(self, card, player):
        suit_to_follow = self.set_suit_to_follow()

        if suit_to_follow is not None:  # checks if suit to follow is None
            print()
            print('suit to follow is ' + suit_to_follow)
            if card.suit is not suit_to_follow:  # checks selected card's suit to see if it matches suit to follow
                print()
                print('card is not suit to follow')
                for card_in_hand in player.hand:  # checks players hand for cards that match suit to follow
                    print()
                    print('checking hand for card that follows suit')
                    if card_in_hand.suit is suit_to_follow:  # player must follow suit, return False and select again
                        print('you have a ' + suit_to_follow + ' in your hand! you must follow suit')
                        return False

                print('playing off suit card')  # shows us that we cannot follow suit, so we can play any card

        self.play_card(card, player)
        return True

    def set_suit_to_follow(self):
        if len(self.board) > 0:
            suit_to_follow = self.board[0].suit
        else:
            suit_to_follow = None
        return suit_to_follow

    def select_highest_card(self):
        card_values = []  # keeps track of card values
        suit_to_follow = self.set_suit_to_follow()
        high_card = None
        for card in self.board:
            if card.suit is not suit_to_follow:
                continue
            else:
                card_values.append(card.RANKS[card.rank])
                if card.RANKS[card.rank] == max(card_values):
                    high_card = card

        self.award_trick(high_card)

    def award_trick(self, high_card):
        for player in plr.Player.List:
            if player.card_played == high_card:
                player.tricks += 1
                print('player ' + str(player.player_number) + ' took the trick with ' + high_card.name)
                print('player ' + str(player.player_number) + ' has ' + str(player.tricks) + ' tricks.')
                player.took_last_trick = True
                print(str(player.took_last_trick) + ' player ' + str(player.player_number))

    def award_points(self):
        for team in plr.Team.List:
            total_tricks = 0

            for player in plr.Player.List:
                if player.team == team:
                    total_tricks += player.tricks

            if total_tricks is 5:
                team.points += 2
            elif total_tricks > 2:
                team.points += 1

    def clean_board(self):  # empties the board list
        for card in self.board[::-1]:
            self.board.remove(card)
            cd.Deck.List.append(card)

    @staticmethod
    def reset_players():
        for player in plr.Player.List:  # resets variable
            player.took_last_trick = False

    @staticmethod
    def clear_trump():
        for eucher_card in cd.Deck.List:
            eucher_card.trump = False
