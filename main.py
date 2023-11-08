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

from colors import print_colors

seed(100)  # make the pseudo-random number generator produce the same output

ASK_OWN_CARD = "%s, choose the index of your card (1..%d): "
ASK_OPP_CARD = "Now choose the index of opp card (1..%d): "
ASK_SKILL = "Activate special ability? (Y/N): "

CLASSES = {
    "Protein": Protein,
    "Vegetable": Vegetable,
    "Dairy": Dairy,
    "Grain": Grain,
    "Fruit": Fruit,
}
FOOD_TABLE = {}
OUTPUT_WIDTH = 62


def read_stats(filepath):
    global FOOD_TABLE

    if filepath.endswith("json"):
        FOOD_TABLE = json.load(open(filepath))
    else:
        """
        Maybe for bonus marks the students must implement their own, custom
        file format and a parser for that format, instead of using json.
        """
        with open(filepath) as stats_file:
            for line in stats_file:
                if line in ["", "\n"]:
                    continue

                if not line.startswith(" "):
                    curr_group = line.strip().replace(":", "")
                    FOOD_TABLE[curr_group] = {}
                else:
                    name, stats = line.split(" | ")
                    name = name.strip()
                    stats = stats.split(" ")
                    FOOD_TABLE[curr_group][name] = {}

                    for i, stat in enumerate(stats):
                        FOOD_TABLE[curr_group][name][Food.STAT_ORDER[i]] = int(stat)


def get_parent_class(item):
    for group, values in FOOD_TABLE.items():
        for food in values:
            if item == food:
                return group
    return None


def generate_food_object(parent_class, food_name, stats, color):
    return CLASSES[parent_class](food_name, stats, color)


def get_player_color(player):
    return print_colors["B"] if player == 0 else print_colors["R"]


def colored_player(player):
    return f"{get_player_color(player)}Player {player+1}{print_colors[None]}"


def build_decks(deck_filepath: str) -> dict[int, list[Food]]:
    decks = [[], []]
    curr_player = -1
    curr_color = "B"
    if deck_filepath.endswith("json"):
        deck_file = json.load(open(deck_filepath))
        curr_player = 0
        for player_number, player_deck in deck_file.items():
            curr_color = "B" if curr_player == 0 else "R"
            for food_item in player_deck:
                parent_class = get_parent_class(food_item)
                stats = FOOD_TABLE[parent_class][food_item]

                food_obj = generate_food_object(
                    parent_class, food_item, stats, curr_color
                )
                decks[curr_player].append(food_obj)
            curr_player += 1
    else:
        """
        Again, maybe a custom deck format reader for bonus marks.
        """
        with open(deck_filepath) as input_decks:
            while input_decks.readable():
                food_name = input_decks.readline().strip()
                if food_name == "":
                    break
                if food_name.find("Player") >= 0:
                    curr_player += 1
                    continue

                food_class = get_parent_class(food_name)
                food_stats = FOOD_TABLE[parent_class][food_item]

                curr_color = "B" if curr_player == 0 else "R"
                food_character = CLASSES[food_class](
                    food_name, stats=food_stats, color=curr_color
                )
                decks[curr_player].append(food_character)

    return decks


def draw_round_num(round_num):
    print(
        f"\n┌{'─'*24}( {print_colors['Y']}ROUND {round_num} {print_colors[None]}){'─'*25}┐\n"
    )


def draw_table_player_name(player):
    width = OUTPUT_WIDTH - 9
    print(f"{' ' * (width // 2)}{colored_player(player)}{' ' * (width // 2)}")


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
    totals = {Food.STAT_ORDER[i]: 0 for i in range(len(Food.STAT_ORDER))}
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


def flip_coin():
    if random() < 0.5:
        print(f"Flipped heads! {colored_player(0)} starts.")
        return 0
    else:
        print(f"Flipped tails! {colored_player(1)} starts.")
        return 1


def ask_player_index(player):
    color = colored_player(player)
    input_str = input(ASK_OWN_CARD % (color, len(decks[player])))
    return int(input_str) - 1 if input_str != "" else None


def ask_opp_index(player):
    input_str = input(ASK_OPP_CARD % len(decks[player]))
    return int(input_str) - 1 if input_str != "" else None


def ask_should_skill():
    return input(ASK_SKILL).lower() == "y"


if __name__ == "__main__":
    stats_file = "config/food_stats.json"
    decks_file = "config/decks.json"
    if len(argv) == 3:
        stats_file = argv[1]
        decks_file = argv[2]

    # Reading in the stats of all food items
    read_stats(stats_file)

    # Reading in the players' decks
    decks = build_decks(decks_file)

    # Start game play loop

    print("Flipping coin to decide who starts...")
    curr_player = flip_coin()

    game_over = False
    round_num = 1
    while not game_over:
        draw_round_num(round_num)

        draw_decks(decks)

        opponent = not curr_player

        index_own = ask_player_index(curr_player)
        if index_own is None:
            print("Player skipped round.")
            curr_player = not curr_player
            round_num += 1
            continue

        index_opp = ask_opp_index(curr_player)
        should_skill = ask_should_skill()
        print()

        card_own = decks[curr_player][index_own]
        card_opp = decks[opponent][index_opp]

        if should_skill:
            card_own.special_ability()
            # activate its ability

        # returns true if opponent card was killed
        if index_opp is not None:
            is_killed = card_own.damage(card_opp)
            if is_killed:
                decks[opponent].pop(index_opp)

        # win condition
        if len(decks[opponent]) == 0:
            print(f"Game is finished! Player {int(opponent)} lost!")
            exit(0)

        curr_player = not curr_player
        round_num += 1
