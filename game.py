from utils import colored_player, flip_coin


class Game:
    def __init__(self):
        """
        Creates a new empty game state object
        """
        self.round_num = 1

    def load_food_table(self, food_table):
        self.food_table = food_table

    def from_table(self, parent_class, food_item):
        return self.food_table[parent_class][food_item]

    def load_decks(self, decks):
        self.decks = decks

    def get_decks(self):
        return self.decks

    def choose_player(self) -> bool:
        self.curr_player = flip_coin()
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
