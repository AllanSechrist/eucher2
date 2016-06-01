"""
game logic goes here
"""

from objects import player as plr
from objects import card as cd


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
            return play_order(player_list, player.player_number)


def assign_play_order():
    player_list = plr.Player.List

    for player in player_list:
        if player.took_last_trick is True:
            return play_order(player_list, player.player_number)
