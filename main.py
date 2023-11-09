import json
import os
import sys
from random import random, seed

import constants
import utils
from classes.food import Food
from colors import print_colors
from game import Game
from gui import Gui

seed(100)  # make the pseudo-random number generator produce the same output


OUTPUT_WIDTH = 62

"""
[============================== CMD INPUT =====================================]
"""

# region


def get_arg_value(name: str) -> str:
    index = sys.argv.index(name)
    return sys.argv[index + 1]


def parse_arguments() -> tuple[str, str, bool]:
    stats_file = "input/foods.json"
    decks_file = "input/deck-1.json"
    gui_mode = False

    # --decks --foods --gui
    if "--decks" in sys.argv:
        decks_file = get_arg_value("--decks")
    if "--foods" in sys.argv:
        stats_file = get_arg_value("--foods")
    if "--gui" in sys.argv:
        gui_mode = True

    return stats_file, decks_file, gui_mode


# endregion

"""
[============================== TABLE PRINT ===================================]
"""

# region


def draw_round_num(round_num):
    print(
        f"\n┌{'─'*24}({print_colors['Y']} ROUND {round_num} {print_colors[None]}){'─'*25}┐\n"
    )


def draw_table_player_name(player):
    width = OUTPUT_WIDTH - 9
    print(f"{' ' * (width // 2)}{utils.colored_player(player)}{' ' * (width // 2)}")


def draw_table_heading_top():
    print(f"├{'─'*4}┬{'─'*15}┬{'─'*7}┬{'─'*7}┬{'─'*7}┬{'─'*7}┬{'─'*7}┤")


def draw_table_heading_text():
    print(
        f"{'│Pos':5s}│ {'Card':13s} │ {'HP':5s} │ {'MP':5s} │ {'ATK':5s} │ {'DEFF':5s} │ {'MS':5s} │"
    )


def draw_table_heading_bottom():
    print(f"├{'─'*4}┼{'─'*15}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}┘")


def draw_table_total_row(deck: list[Food]):
    print(f"├{'─'*4}┼{'─'*15}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}")
    totals = {constants.STAT_ORDER[i]: 0 for i in range(len(constants.STAT_ORDER))}
    print(f"│{' ':4s}│ {'Total':14s}", end="")
    for i, obj in enumerate(deck):
        for stat in obj.stats:
            totals[stat] += obj.get(stat)
    for total in totals:
        print(f"│ {totals[total]:5.1f} ", end="")
    print()


def draw_deck(deck: list[Food], player):
    box_chars = "─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼".split(" ")
    draw_table_player_name(player)
    draw_table_heading_top()
    draw_table_heading_text()
    draw_table_heading_bottom()
    for pos, character in enumerate(deck):
        print(f"│{pos+1:-3d} │ {character.get_table_row()}")
    draw_table_total_row(deck)
    print()


def draw_decks(decks):
    for player in range(2):
        draw_deck(decks[player], player)


def update_str(round_num, decks):
    draw_round_num(round_num)
    draw_decks(decks)


# endregion


if __name__ == "__main__":
    stats_file, decks_file, gui_mode = parse_arguments()
    game = Game(gui_mode)
    if game.gui_mode:
        gui = Gui(game)

    # Reading in the files
    game.load_stats(stats_file)
    game.load_decks(decks_file)

    # Start game play loop
    game.choose_player()
    while True:
        # drawing phase
        if game.gui_mode:
            gui.update()
        else:
            update_str(game.get_round(), game.get_decks())

        # input phase
        if game.gui_mode:
            index_own = gui.get_index_own()
            index_opp = gui.get_index_opp()
            gui.draw_active_ability_button()
            should_skill = gui.should_skill()
        else:  # text mode
            index_own = game.ask_index_own()
            index_opp = game.ask_index_opp()
            should_skill = game.should_skill()
            print()

        # action phase
        card_own = game.decks[game.get_player()][index_own]

        if should_skill:  # player chose to activate ability
            print("activating ability")
            card_own.special_ability()

        if index_opp is not None:  # player chose a card to attack
            card_opp = game.decks[game.get_opponent()][index_opp]
            game.handle_attack(card_own, card_opp, index_opp)

        # win condition
        if len(game.decks[game.get_opponent()]) == 0:
            print(f"Game is finished! Player {int(game.get_opponent())} lost!")
            exit(0)

        game.next_round()
