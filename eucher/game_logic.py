"""
game logic goes here
"""

from objects import player as plr
from objects import card as cd
import random


def play_order(list, number):
    play_order = [list[(number - 1) % 4],
                  list[number % 4],
                  list[number + 1] % 4,
                  list[number + 2] % 4]
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
            return play_order(player_list, player.player_number)


def assign_dealer(count):
    if count < 1:
        dealer = random.choice(plr.Player.List)  # assign random person to be dealer at the game start
        dealer.dealer = True
        count += 1  # keeps track of number of rounds(may be changed later to a boolean for the start of the game)
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

    def __init__(self):
        self.top_card = cd.Deck.List[0]
        assign_dealer(0)
        self.play_order = assign_deal_order()

    def loop(self):  # manages class methods
        done = False
        while not done:
            print(self.top_card.suit)
            done = self.pass_or_call()

    def make_suit_trump(self, suit):
        pass

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

    def get_player_input(self, player):
        player_input = input('player ' + str(player.player_number) + ' PASS or TRUMP? :').upper()
        return player_input

    def pick_up_trump(self):
        dealers_hand = self.play_order[3].hand

        dealers_hand.append(self.top_card)  # adds the top card of the kitty ot the dealers hand
        cd.Deck.List.remove(self.top_card)  # removes top card from the kitty

        for card in dealers_hand:
            print(card.name)

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

                            if trump_input == suit and suit != self.top_card:
                                print(suit + ' has been made trump')
                                self.make_suit_trump(trump_input)  # make selected suit trump
                                return True
                            elif trump_input == self.top_card:
                                print('You cannot call that trump')
                                break

                else:
                    print('invalid input')

