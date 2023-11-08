from classes.food import Food


"""
This class of foods are very versatile and are supports for other food types.
"""


class Vegetable(Food):
    def __str__(self):
        return f"{self.color}{self.name} (Vegetable Class)\033[0m"

    def special_ability(self, other=None):
        print(f"{self} is activating its special ability!")
