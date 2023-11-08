from random import random
from colors import print_colors

from constants import STATS_MIN, STATS_MAX


class Food:
    DEFLECTED_STR = "  Deflected %.1f damage (%.1f -> %.1f)"
    DODGE_STR = "  Dodge chance: %.1f%%"
    HEALTH_STR = "  %s's heath updated: %.1f -> %.1f"

    def __init__(self, food_item, stats, color):
        self.name = food_item
        self.stats = stats
        self.color = print_colors[color]
        self.dodge_rate = 1 - (1 / (1 + self.stats["speed"] / STATS_MAX["speed"]))

    def get(self, attribute):
        return self.stats[attribute]

    def damage(self, other):
        print(f"{self} is attacking {other}!")
        return other.defend(self)

    def calc_deflected_damage(self, opp_dmg):
        deff_percentage = self.stats["defence"] / 100
        return round(deff_percentage * opp_dmg, 1)

    def can_dodge(self):
        print(self.DODGE_STR % (self.dodge_rate * 100))
        return random() < self.dodge_rate

    def defend(self, other):
        prev_health = self.stats["health"]
        opp_dmg = other.get("attack")

        has_dodged = self.can_dodge()
        if has_dodged:
            print(f"  Completely dodged incoming attack!")
            print(f"  Health remained at {self.stats['health']:.1f}")
            return

        deflected = self.calc_deflected_damage(opp_dmg)

        print(self.DEFLECTED_STR % (deflected, opp_dmg, opp_dmg - deflected))
        # f"  Deflected {deflected:.1f} damage ({opp_dmg:.1f} -> {opp_dmg - deflected:.1f})"
        # )
        self.stats["health"] -= opp_dmg - deflected
        print(self.HEALTH_STR % (self, prev_health, self.stats["health"]))

        if self.stats["health"] <= 0:
            print(f"  {self} is now dead...")
            return True

        return False

    # def special_ability(self):
    # print("  {self} activating special ability!")

    def get_table_row(self):
        output_str = f"{self.name:13s} "
        for key in self.stats:
            output_str += f"│ {self.stats[key]:5.1f} "
        return output_str

    def __str__(self):
        return f"{self.color}"
