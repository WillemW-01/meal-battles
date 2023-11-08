from food import Food


"""
This class of foods are heavy hitters and big tanks.
They have low mana pools and are very slow in general.

Meat products' special ability is <insert name>.
"""


class Protein(Food):
    def __init__(self, food_item, stats, color):
        super().__init__(food_item, stats, color)

    def __str__(self):
        return f"{self.color}{self.name} (Meat Class)\033[0m"

    def special_ability(self, other=None):
        print(f"{self} is activating its special ability!")
