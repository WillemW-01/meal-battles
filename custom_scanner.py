from main import FOOD_TABLE, CLASSES, get_parent_class
from constants import STAT_ORDER
from classes.food import Food


def load_stats(stats_file: str) -> dict[str, dict[str, dict[str, int]]]:
    """
    Students can maybe get bonus marks for implementing their own format
    and code their own parser for it, instead of using json.
    """
    if stats_file.endswith("conf"):
        temp_table = {}
        with open(stats_file) as stats_file:
            for line in stats_file:
                if line in ["", "\n"]:
                    continue

                if not line.startswith(" "):
                    curr_group = line.strip().replace(":", "")
                    temp_table[curr_group] = {}
                else:
                    name, stats = line.split(" | ")
                    name = name.strip()
                    stats = stats.split(" ")
                    temp_table[curr_group][name] = {}

                    for i, stat in enumerate(stats):
                        temp_table[curr_group][name][STAT_ORDER[i]] = int(stat)

        return temp_table
    else:
        exit("ERR: invalid file format.")


def build_decks(deck_filepath: str) -> dict[int, list[Food]]:
    """
    Again, maybe a custom deck format reader for bonus marks.
    """
    if deck_filepath.endswith("deck"):
        decks = [[], []]
        curr_player = -1
        curr_color = "B"
        with open(deck_filepath) as input_decks:
            for line in input_decks:
                food_name = line.strip()
                if food_name == "":
                    break
                if food_name.find("Player") >= 0:
                    curr_player += 1
                    continue

                parent_class = get_parent_class(food_name)
                food_stats = FOOD_TABLE[parent_class][food_name]

                curr_color = "B" if curr_player == 0 else "R"
                food_character = CLASSES[parent_class](
                    food_name, stats=food_stats, color=curr_color
                )
                decks[curr_player].append(food_character)
        return decks
    else:
        exit("ERR: invalid file format.")
