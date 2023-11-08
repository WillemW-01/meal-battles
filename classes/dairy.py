from classes.food import Food


"""
This class of foods are very absorbant to damage, although don't have that
many hit points.
"""


class Dairy(Food):
    def __str__(self):
        return f"{self.color}{self.name} (Dairy Class)\033[0m"

    def special_ability(self, other=None):
        print(f"{self} is activating its special ability!")
