import json

from classes.dairy import Dairy
from classes.food import Food
from classes.fruit import Fruit
from classes.grain import Grain
from classes.protein import Protein
from classes.vegetable import Vegetable
from constants import STAT_ORDER
from utils import colored_player, flip_coin


class Game:
    TEMPLATES = json.load(open("template_strings.json"))

    CLASSES = {
        "Protein": Protein,
        "Vegetable": Vegetable,
        "Dairy": Dairy,
        "Grain": Grain,
        "Fruit": Fruit,
    }

    def generate_food_object(self, parent_class, food_name, stats, color):
        return self.CLASSES[parent_class](food_name, stats, color)

    def __init__(self, gui_mode):
        """
        Creates a new empty game state object
        """
        self.round_num = 1
        self.gui_mode = gui_mode

    def load_stats(self, stats_file: str) -> dict[str, dict[str, dict[str, int]]]:
        """
        Loads in the configuration file of the stats belonging to each food item,
        and to which food group they belong.

        Students can maybe get bonus marks for implementing their own format
        and code their own parser for it, instead of using json.
        """

        if stats_file.endswith("json"):
            self.food_table = json.load(open(stats_file))
        elif stats_file.endswith("conf"):
            self.food_table = {}
            with open(stats_file) as stats_file:
                for line in stats_file:
                    if line in ["", "\n"]:
                        continue

                    if not line.startswith(" "):
                        curr_group = line.strip().replace(":", "")
                        self.food_table[curr_group] = {}
                    else:
                        name, stats = line.split(" | ")
                        name = name.strip()
                        stats = stats.split(" ")
                        self.food_table[curr_group][name] = {}

                        for i, stat in enumerate(stats):
                            self.food_table[curr_group][name][STAT_ORDER[i]] = int(stat)
        else:
            exit("ERR: invalid file format.")

    def load_decks(self, deck_filepath: str) -> dict[int, list[Food]]:
        """
        Function for reading in the deck files. Json implementation needs a little
        bit more code than just .load() since the objects need to be created.
        """

        self.decks = [[], []]
        curr_player = -1
        curr_color = "B"
        if deck_filepath.endswith("json"):
            deck_file = json.load(open(deck_filepath))
            curr_player = 0
            for player_number, player_deck in deck_file.items():
                curr_color = "B" if curr_player == 0 else "R"
                for food_item in player_deck:
                    parent_class = self.get_parent_class(food_item)
                    stats = self.from_table(parent_class, food_item)

                    food_obj = self.generate_food_object(
                        parent_class, food_item, stats, curr_color
                    )
                    self.decks[curr_player].append(food_obj)
                curr_player += 1

        elif deck_filepath.endswith("deck"):
            with open(deck_filepath) as input_decks:
                for line in input_decks:
                    food_name = line.strip()
                    if food_name == "":
                        break
                    if food_name.find("Player") >= 0:
                        curr_player += 1
                        continue

                    parent_class = self.get_parent_class(food_name)
                    food_stats = self.from_table(parent_class, food_name)

                    curr_color = "B" if curr_player == 0 else "R"
                    food_character = self.CLASSES[parent_class](
                        food_name, stats=food_stats, color=curr_color
                    )
                    self.decks[curr_player].append(food_character)
        else:
            exit("ERR: invalid file format.")

    def from_table(self, parent_class, food_item):
        return self.food_table[parent_class][food_item]

    def get_decks(self):
        return self.decks

    def choose_player(self) -> bool:
        if not self.gui_mode:
            print("Flipping coin to decide who starts...")
        self.curr_player = flip_coin()
        if not self.gui_mode:
            if self.curr_player:
                print(f"Flipped heads! {colored_player(1)} starts.")
            else:
                print(f"Flipped tails! {colored_player(0)} starts.")

    def get_player(self) -> bool:
        return self.curr_player

    def change_player(self):
        self.curr_player = not self.curr_player

    def get_opponent(self):
        return not self.curr_player

    def get_round(self) -> int:
        return self.round_num

    def increment_round(self):
        self.round_num += 1

    def next_round(self):
        self.change_player()
        self.increment_round()

    def get_parent_class(self, item):
        for group, values in self.food_table.items():
            for food in values:
                if item == food:
                    return group
        return None

    def ask_index_own(self):
        color = colored_player(self.curr_player)
        input_str = input(
            self.TEMPLATES["ASK_OWN_CARD"] % (color, len(self.decks[self.curr_player]))
        )
        return int(input_str) - 1 if input_str != "" else None

    def ask_index_opp(self):
        input_str = input(
            self.TEMPLATES["ASK_OPP_CARD"] % len(self.decks[self.get_opponent()])
        )
        return int(input_str) - 1 if input_str != "" else None

    def should_skill(self):
        return input(self.TEMPLATES["ASK_SKILL"]).lower() == "y"

    def handle_attack(self, card_own, card_opp, index_opp):
        is_killed = card_own.damage(card_opp)
        if is_killed:
            self.decks[self.get_opponent()].pop(index_opp)
