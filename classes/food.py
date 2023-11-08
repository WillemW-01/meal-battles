from random import random
from colors import print_colors


class Food:
    name = ""
    stat_order = ["health", "mana", "attack", "defence", "speed"]

    def __init__(self, food_item, stats, color):
        self.name = food_item
        self.stats = stats
        self.color = print_colors[color]
        
    def get(self, attribute):
        return self.stats[attribute]

    def damage(self, other):
        return other.defend(self)

    def defend(self, other):
        prev_health = self.stats["health"]
        print(f"{self} is being attacked by {other}!")
        r = random() * 10
        # print(f"rolled {r:.2f}")
        if r < self.stats['speed']:
            print(f"  Dodged incoming attack!")
            print(f"  Health remained at {self.stats['health']}")
            return

        deflected = round(self.stats["defence"] / 10 * other.get("attack"), 2)

        print(f"  Deflected {deflected} damage")
        self.stats["health"] -= other.get("attack") - deflected
        print(f"  {self}'s heath updated: {prev_health} -> {self.stats['health']}")

        if self.stats["health"] <= 0:
            print(f"  {self} is now dead...")
            return True

        return False

    def full_name(self):
        return (
            f"{self.name:13s} │ {self.stats['health']:5.2f} │ {self.stats['mana']:5.2f} │ "
            f"{self.stats['attack']:5.2f} │ {self.stats['defence']:5.2f} │ {self.stats['speed']:5.2f}"
        )

    def __str__(self):
        return f"{self.color}"
