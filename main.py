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
import json

from food import Food
from protein import Protein
from fruit import Fruit
from dairy import Dairy
from grain import Grain
from vegetable import Vegetable

from colors import print_colors

seed(100)  # make the pseudo-random number generator produce the same output

ASK_OWN_CARD = "%s, choose the index of your card (1..%d): "
ASK_OPP_CARD = "Now choose the index of opp card (1..%d): "
ASK_SKILL = "Special ability? (Y/N): "

CLASSES = {
    "Protein": Protein,
    "Vegetable": Vegetable,
    "Dairy": Dairy,
    "Grain": Grain,
    "Fruit": Fruit,
}

FOOD_TABLE = {}


def read_stats(filepath):
    global FOOD_TABLE

    if filepath.endswith("json"):
        FOOD_TABLE = json.load(open(filepath))
    else:
        """
        Maybe for bonus marks the students must implement their own, custom
        file format and a parser for that format, instead of using json.
        """
        stat_order = ["health", "mana", "attack", "defence", "speed"]
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
                        FOOD_TABLE[curr_group][name][stat_order[i]] = int(stat)


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


def build_decks(deck_filepath):
    decks = [[], []]
    curr_player = -1
    curr_color = "B"
    if deck_filepath.endswith("json"):
        deck_file = json.load(open(deck_filepath))
        curr_player = 0
        for player_number, player_deck in deck_file.items():
            for food_item in player_deck:
                parent_class = get_parent_class(food_item)
                stats = FOOD_TABLE[parent_class][food_item]
                curr_color = "B" if curr_player == 0 else "R"

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


def table_draw_label_top():
    print(f"{'─'*4}┬{'─'*15}┬{'─'*7}┬{'─'*7}┬{'─'*7}┬{'─'*7}┬{'─'*7}┐")


def table_draw_heading():
    print(
        f"{'Pos':4s}│ {'Card':14s}│ {'HP':5s} │ {'MP':5s} │ {'ATK':5s} │ {'DEFF':5s} │ {'MS':5s} │"
    )


def table_draw_label_bottom():
    print(f"{'─'*4}┼{'─'*15}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}┼{'─'*7}┘")


def print_deck(deck: list[Food], player):
    box_chars = "─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼".split(" ")
    print(f"{colored_player(player)}'s deck:")
    table_draw_label_top()
    table_draw_heading()
    table_draw_label_bottom()
    for pos, character in enumerate(deck):
        print(f"{pos+1:-3d} │ {character.full_name()}")
    print()


def print_decks(decks):
    for player in range(2):
        print_deck(decks[player], player)


def ask_player_index(player):
    color = colored_player(curr_player)
    return int(input(ASK_OWN_CARD % (color, len(decks[curr_player])))) - 1


if __name__ == "__main__":
    stats_file = "config/food_stats.json"
    decks_file = "config/decks.json"
    if len(argv) == 3:
        stats_file = argv[1]
        decks_file = argv[2]

    # Reading in the stats of all food items
    read_stats(stats_file)
    print("Done reading in statistics and groups")

    # Reading in the players' decks
    decks = build_decks(decks_file)
    print("Done reading decks")

    # Start game play loop
    curr_player = 0

    print("Flipping coin to decide who starts...")

    if random() < 0.5:
        print(f"Flipped heads! {colored_player(0)} starts.")
    else:
        print(f"Flipped tails! {colored_player(1)} starts.")
        curr_player = 1

    game_over = False
    round_num = 1
    while not game_over:
        print(f"[{'='*27} ROUND {round_num} {'='*27}]\n")

        print_decks(decks)

        opponent = not curr_player

        index_own = (
            int(
                input(
                    ASK_OWN_CARD
                    % (colored_player(curr_player), len(decks[curr_player]))
                )
            )
            - 1
        )
        index_opp = int(input(ASK_OPP_CARD % len(decks[curr_player]))) - 1
        should_skill = input(ASK_SKILL).lower() == "y"
        print()

        card_own = decks[curr_player][index_own]
        card_opp = decks[opponent][index_opp]

        if should_skill:
            print(f"{card_own} is activating its ability!")
            # activate its ability

        # returns true if opponent card was killed
        is_killed = card_own.damage(card_opp)
        if is_killed:
            decks[opponent].pop(index_opp)

        # win condition
        if len(decks[opponent]) == 0:
            print(f"Game is finished! Player {int(opponent)} lost!")
            exit(0)

        print()

        curr_player = not curr_player
        round_num += 1
