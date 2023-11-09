# Meal Battles

    Food-themed, turn-based card battler

## Description:

The food we eat each have their own distribution of macronutrients.
These macronutrients can be compared to the stats of the food, and when we plan
meals, optimally we would want to make the stats as balanced as possible.

Enter **Meal Battles**, the turn-based, card battler that will take two decks of
food items. The idea is simple: the food cards each have their own stats, and these
cards can be combined into meals (decks) such that each player must try to remove
all the cards from their opponent's deck. More information is found below.

## Nutrients compared to RPG stats

The macronutrients of foods include calories, carbohydrates, proteins, lipids and fibre.
Each of these macronutrients can be compared in the following way:

| Stat                | Nutrient      | Real world use                                                                                  | Use in game                                                                                                     |
| ------------------- | ------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Health (HP)         | Calories      | This is due to the amount of energy the food provides can influence a person's ability to work. | Health points determine how many hits a food character can take.                                                |
| Mana (MP)           | Carbohydrates | Carbohyrates are the main source of energy for the body, but more importantly the brain.        | Mana points determine the amount and degree of spells (special abilities) that can be cast by a food character. |
| Damage (DMG)        | Protein       | Proteins are used to rebuild and grow muscles, which correlates to strength.                    | Attack contributes to the damage outputted by a food character.                                                 |
| Defence (DEFF)      | Lipids        | Having more fat reserves around the organs protects them.                                       | Defence determines how much % of incoming damage a food character deflects.                                     |
| Movement Speed (MS) | Fibre         | Fibre prevents constipation by assisting in moving food around the body.                        | Movement speed postiively correlates to the chances of completely missing a direct attack (not spells).         |

## Game loop

The food items that are used are stored in a `foods` configuration file, and the players' decks are also loaded into another configuration file.
These files are read at the start of the game.
Then, a player is chosen at random to start, and the player must choose one of their own cards to attack one of their opponent's cards. They may also choose to activate their card's special ability. The player may also choose not to attack an opponent's card. Then, if chosen, the player's card will attack the opponent's card and the battle result will be displayed. A new round will begin after that, and the opponent has their turn. This continues until a player's deck is empty.

## Implementation so far

For now, in this demo project, around 50 different foods will be implemented with their
respective food groups, and a shallow gameplay loop will be programmed.

This game can also support text mode and graphics mode, with an appropriate cmd switch.

See the `ideas` folder for more information on possible ways the project can
go forward, as well as documentation for how certain parts of the program _should_ work.

## Execution

All arguments are optional, and can be in any order.

`$ python main.py [--foods <filepath>] [--decks <filepath] [--gui]`

Defaults are as follows:

- foods: `input\foods.json`
- decks: `input\deck-1.json`

(see `input` folder for example inputs)
