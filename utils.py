from random import random

from colors import print_colors


def get_player_color(player):
    return print_colors["B"] if player == 0 else print_colors["R"]


def colored_player(player):
    return f"{get_player_color(player)}Player {player+1}{print_colors[None]}"


def flip_coin():
    return random() > 0.5
