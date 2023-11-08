"""
Title:
Meal Battles - Battle Arena for Food Classes

Idea:
The food we eat all have values related to their nutrition, among them calories, 
carbohydrates, proteins, lipids and fibre. These can also be seen as stats like 
those found in RPGs. For example, the following comparisons can be made:

1. Health (HP) ==> calories
   This is due to the amount of energy the food provides can influence a person's 
   ability to work.
   Health points determine how many hits a food character can take.
2. Mana (MP) ==> carbohydrates
   Carbohyrates are the main source of energy for the body, but more importantly 
   the brain.
   Mana points determine the amount and degree of spells (special abilities) that
   can be cast by a food character.
3. Damage (DMG) ==> protein
   Proteins are used to rebuild and grow muscles, which correlates to strength.
   Attack contributes to the damage outputted by a food character.
4. Defence (DEFF) ==> lipids
   Having more fat reserves around the organs protects them.
   Defence determines how much % of incoming damage a food character deflects.
5. Movement Speed (MS) ==> fibre
   Fibre prevents constipation by assisting in moving food around the body.
   Movement speed postiively correlates to the chances of completely missing
   a direct attack (not spells).
    
Due to these comparisons, the idea of having different foods being represented
as characters in an RPG-type game is not far off. Different foods will have 
different strengths, and different foods can also be grouped together in their 
respected food group (meat, grains, dairy) which could all have specific buffs
and drawbacks. Different foods can then inherit the traits of their food group,
and can be put together in a meal. Once a player has put together a meal, they 
can fight against another player's meal. This can be accomplished via a 
turn-based system. The exact details is still being thought out.

For now, in this demo project, 6 different foods will be implemented with their
respective food groups, and a very shallow game-play loop will be programmed.

This game can also support text mode and graphics mode, if a GUI or only a text
mode would be desired or necessary at one stage (for example 2 hand-ins)
"""

from random import random, seed
from sys import argv
import os
import json

from classes.food import Food
from classes.protein import Protein
from classes.fruit import Fruit
from classes.dairy import Dairy
from classes.grain import Grain
from classes.vegetable import Vegetable
from game import Game
from gui import Gui
import constants
import custom_scanner
import utils

from colors import print_colors

seed(100)  # make the pseudo-random number generator produce the same output

templates = json.load(open("template_strings.json"))

CLASSES = {
    "Protein": Protein,
    "Vegetable": Vegetable,
    "Dairy": Dairy,
    "Grain": Grain,
    "Fruit": Fruit,
}
OUTPUT_WIDTH = 62

"""
[============================== FILE INPUT ====================================]
"""

# region


def read_stats(stats_file: str) -> dict[str, dict[str, dict[str, int]]]:
    """
    Loads in the configuration file of the stats belonging to each food item,
    and to which food group they belong.

    Students can maybe get bonus marks for implementing their own format
    and code their own parser for it, instead of using json.
    """

    if stats_file.endswith("json"):
        return json.load(open(stats_file))
    else:
        return custom_scanner.load_stats(stats_file)


def build_decks(deck_filepath: str) -> dict[int, list[Food]]:
    """
    Function for reading in the deck files. Json implementation needs a little
    bit more code than just .load() since the objects need to be created.

    Students can again create their own format and make their own parser for it.
    """

    decks = [[], []]
    curr_player = -1
    curr_color = "B"
    if deck_filepath.endswith("json"):
        deck_file = json.load(open(deck_filepath))
        curr_player = 0
        for player_number, player_deck in deck_file.items():
            curr_color = "B" if curr_player == 0 else "R"
            for food_item in player_deck:
                parent_class = game.get_parent_class(food_item)
                stats = game.from_table(parent_class, food_item)

                food_obj = generate_food_object(
                    parent_class, food_item, stats, curr_color
                )
                decks[curr_player].append(food_obj)
            curr_player += 1
    else:
        decks = custom_scanner.build_decks(deck_filepath)

    return decks


# endregion


"""
[============================== USER INPUT ====================================]
"""

# region


def ask_player_index(player):
    color = utils.colored_player(player)
    input_str = input(templates["ASK_OWN_CARD"] % (color, len(decks[player])))
    return int(input_str) - 1 if input_str != "" else None


def ask_opp_index(player):
    input_str = input(templates["ASK_OPP_CARD"] % len(decks[player]))
    return int(input_str) - 1 if input_str != "" else None


def ask_should_skill():
    return input(templates["ASK_SKILL"]).lower() == "y"


# endregion


"""
[================================= HELPER =====================================]
"""
# region


def generate_food_object(parent_class, food_name, stats, color):
    return CLASSES[parent_class](food_name, stats, color)


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


# endregion


if __name__ == "__main__":
    stats_file = "input/food_stats.json"
    decks_file = "input/decks.json"
    if len(argv) == 3:
        stats_file = argv[1]
        decks_file = argv[2]

    game = Game()

    # Reading in the stats of all food items
    food_table = read_stats(stats_file)
    game.load_food_table(food_table)

    # Reading in the players' decks
    decks = build_decks(decks_file)
    game.load_decks(decks)

    gui = Gui(game)

    # Start game play loop

    print("Flipping coin to decide who starts...")
    game.choose_player()

    while True:
        # drawing phase
        gui.update()
        exit(1)
        draw_round_num(game.get_round())
        draw_decks(game.get_decks())

        # input phase
        index_own = ask_player_index(game.get_player())
        if index_own is None:
            print("Player skipped round.")
            game.next_round()
            continue

        index_opp = ask_opp_index(game.get_player())
        should_skill = ask_should_skill()
        print()

        card_own = decks[game.get_player()][index_own]
        card_opp = decks[game.get_opponent()][index_opp]

        # action phase
        if should_skill:
            card_own.special_ability()
            # activate its ability

        # returns true if opponent card was killed
        if index_opp is not None:
            is_killed = card_own.damage(card_opp)
            if is_killed:
                decks[game.get_opponent()].pop(index_opp)

        # win condition
        if len(decks[game.get_opponent()]) == 0:
            print(f"Game is finished! Player {int(game.get_opponent())} lost!")
            exit(0)

        game.next_round()
