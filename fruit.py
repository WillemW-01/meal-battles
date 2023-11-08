from food import Food

class Fruit(Food):
    """
    **High**: defence (lipids) + damage (protein)

    **Low**: health (calories) + mana (carbohydrates)

    They have spells that can heal, regenerate, or poison allies or enemies.

    Examples of dairy characters are milk, cheese, yogurt, and butter.
    """
    def __str__(self):
        return f"{self.color}{self.name} (Fruit Class)\033[0m"

    def special_ability(self, other):
        print("Performing special ability!")
