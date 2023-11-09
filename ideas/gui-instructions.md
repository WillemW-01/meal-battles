# Instructions for GUI functionality

The main loop of the GUI must follow this exactly:

1. The program must wait for player to left-click on one of their own cards
   - If player right-clicks at any time on any card, the program must display
     additional information about that card on the bottom of the screen.
   - The program must reject left clicks on their opponent's cards
2. The program must then wait for the player to left-click on one of their opponent's cards
   - Again, any right clicks are handled as above
   - The program may accept left clicks on cards, which means no opp card is attacked
3. The program must wait for the player to either left-click on the ability button, or somewhere else
   - If the player left-clicks anywhere else than the ability button, the ability is not played
   - Otherwise, the ability is activated
4. The own card activates its ability if 3 was successful
5. Then, the own card attacks the opp card if 2 was successful
6. Then, the other player has their turn and the round number is increased

These steps ensure that the text mode of input can be preserved, and the code in main
does not have to change:

```
card_own = ask_own_index()
card_opp = ask_opp_index()
should_skill = ask_should_skill()

if should_skill: activate_ability()
if card_opp is not None: card_own.attack(card_opp)

game.next_round()
```
