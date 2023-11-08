# Meal Battles

## Food-themed, turn-based card battler

## Description:

The food we eat all have values related to their nutrition, among them calories,
carbohydrates, proteins, lipids and fibre. These can also be seen as stats like
those found in RPGs. For example, the following comparisons can be made:

**1. Health (HP) ==> calories**

This is due to the amount of energy the food provides can influence a person's
ability to work.

Health points determine how many hits a food character can take.

**2. Mana (MP) ==> carbohydrates**

Carbohyrates are the main source of energy for the body, but more importantly
the brain.

Mana points determine the amount and degree of spells (special abilities) that
can be cast by a food character.

**3. Damage (DMG) ==> protein**

Proteins are used to rebuild and grow muscles, which correlates to strength.
Attack contributes to the damage outputted by a food character.

**4. Defence (DEFF) ==> lipids**

Having more fat reserves around the organs protects them.

Defence determines how much % of incoming damage a food character deflects.

**5. Movement Speed (MS) ==> fibre**

Fibre prevents constipation by assisting in moving food around the body.

Movement speed postiively correlates to the chances of completely missing
a direct attack (not spells).

---

Due to these comparisons, the idea of having different foods being represented
as characters in an RPG-type game is not far off. Different foods will have
different strengths, and different foods can also be grouped together in their
respected food group (meat, grains, dairy) which could all have specific buffs
and drawbacks. Different foods can then inherit the traits of their food group,
and can be put together in a meal. Once a player has put together a meal, they
can fight against another player's meal. This can be accomplished via a
turn-based system. The exact details is still being thought out.

For now, in this demo project, 6 different foods will be implemented with their
respective food groups, and a very shallow game-play loop will be programmed.

This game can also support text mode and graphics mode, if a GUI or only a text
mode would be desired or necessary at one stage (for example 2 hand-ins)

See the `ideas` folder for more information on possible ways the project can
go forward.

## Execution

`$ python main.py <food_configuration.json> <decks.json>`

(see `config` folder for example inputs)
