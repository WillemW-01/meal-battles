from classes.food import Food


"""
This class of foods are fast and have lots of mana.
"""


class Grain(Food):
    def __str__(self):
        return f"{self.color}{self.name} (Grain Class)\033[0m"

    def special_ability(self, other=None):
        print(f"{self} is activating its special ability!")
