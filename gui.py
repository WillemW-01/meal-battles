import stdlib.stddraw as stddraw
from area import Area
from game import Game
from gui_constants import *
from stdlib.picture import Picture


class Gui:
    @staticmethod
    def draw_filled_rect(x, y, w, h, fill_color=stddraw.LIGHT_GRAY):
        stddraw.setPenColor(fill_color)
        stddraw.filledRectangle(x, y, w, h)
        stddraw.setPenColor()
        stddraw.rectangle(x, y, w, h)

    def __init__(self, game_state: Game, w=WIDTH, h=HEIGHT):
        stddraw.setCanvasSize(w, h)
        stddraw.setXscale(0, w)
        stddraw.setYscale(0, h)
        stddraw.setFontFamily("Verdana")
        stddraw.setFontSize(30)

        self.game = game_state

        # fmt:off
        self.areas = {
          "deck_1":  Area(DECK_1_L, DECK_1_R, DECK_1_B, DECK_1_T),
          "deck_2":  Area(DECK_2_L, DECK_2_R, DECK_2_B, DECK_2_T),
          "ability":  Area(ABILITY_L, ABILITY_R, ABILITY_B, ABILITY_T),
        }  # fmt:on

    def is_in(self, area_name, x, y):
        return self.areas[area_name].is_clicked(x, y)

    # def _draw_log(self):
    # Gui.draw_filled_rect(LOG_L, LOG_B, LOG_W, LOG_H)
    # pass

    def _draw_top_info(self):
        Gui.draw_filled_rect(INFO_TOP_L, INFO_TOP_B, INFO_TOP_W, INFO_TOP_H)

        curr_player = self.game.get_player()
        player_text = f"Player {int(curr_player) + 1}"
        round_text = f"Round {self.game.get_round()}"
        x_1 = INFO_TOP_L + INFO_TOP_W // 4
        x_2 = INFO_TOP_L + (3 * INFO_TOP_W // 4)
        y = INFO_TOP_B + INFO_TOP_H // 2
        stddraw.text(x_1, y, round_text)
        stddraw.setPenColor(PLAYER_COLORS[curr_player])
        stddraw.text(x_2, y, player_text)
        stddraw.setPenColor()

    def _draw_bottom_info(self):
        Gui.draw_filled_rect(INFO_BOT_L, INFO_BOT_B, INFO_BOT_W, INFO_BOT_H)

    def _draw_ability_button(self, is_active=False):
        print(ABILITY_L, ABILITY_B, ABILITY_W, ABILITY_H)
        Gui.draw_filled_rect(ABILITY_L, ABILITY_B, ABILITY_W, ABILITY_H)

        x_mid = ABILITY_L + ABILITY_W // 2
        y_mid = ABILITY_B + ABILITY_H // 2
        filepath = "images/ability.png" if is_active else "images/ability_2.png"
        stddraw.picture(Picture(filepath), x_mid, y_mid)

    def draw_active_ability_button(self):
        self._draw_ability_button(True)

    def _draw_card(self, left, bottom, side):
        center_x = left + CARD_W // 2
        center_y = bottom + CARD_H // 2
        color = PLAYER_COLORS[side]
        stddraw.setPenColor(color)
        stddraw.filledCircle(center_x, center_y, CARD_W // 4)
        stddraw.setPenColor()

    def _draw_deck_grid(self, left, side):
        stddraw.setPenRadius(1.5)

        # draw the middle line
        stddraw.line(left + CARD_W, DECK_1_T, left + CARD_W, DECK_1_B)

        # draw the lines and the cards for each of the 3 rows
        for row in range(DECK_1_B, DECK_1_T - CARD_H // 2, CARD_H):
            if row > DECK_1_B and row < DECK_1_T - 1:
                stddraw.line(left + 1, row, left + DECK_1_W, row)

            # for now each card is a circle
            self._draw_card(left, row, side)  # left col
            self._draw_card(left + CARD_W, row, side)  # right col

        stddraw.setPenRadius()

    def _draw_decks(self):
        # draw player 1 deck
        Gui.draw_filled_rect(DECK_1_L, DECK_1_B, DECK_1_W, DECK_1_H)
        self._draw_deck_grid(DECK_1_L, False)

        # draw player 2 deck
        Gui.draw_filled_rect(DECK_2_L, DECK_2_B, DECK_2_W, DECK_2_H)
        self._draw_deck_grid(DECK_2_L, True)

    def get_mouse_click(self):
        while True:
            stddraw.show(UPDATE_SPEED)
            if stddraw.mousePressed():
                side = stddraw.mouseSide()
                return side == "left", stddraw.mousePos()

    def get_left_click(self):
        side, pos = self.get_mouse_click()
        while not (side == Gui.MOUSE_LEFT):
            if side == Gui.MOUSE_RIGHT:
                print("clicked info of something")
            side, pos = self.get_mouse_click()

        # we know side == MOUSE_LEFT
        return pos

    def get_index(self, area):
        pos = self.get_left_click()
        in_deck_area = self.is_in(area, *pos)
        while not in_deck_area:
            pos = self.get_left_click()
            in_deck_area = self.is_in(area, *pos)
        return pos

    def get_index_own(self):
        deck_indexes = ["deck_1", "deck_2"]
        own_area = deck_indexes[self.game.get_player()]
        pos = self.get_index(own_area)

        print("clicked on own card")

    def get_index_opp(self):
        deck_indexes = ["deck_1", "deck_2"]
        opp_area = deck_indexes[not self.game.get_player()]
        pos = self.get_index(opp_area)

        print("clicked on opp card")

    def should_skill(self):
        pos = self.get_left_click()
        return self.is_in("ability", *pos)

    def update(self):
        # self._draw_log()
        self._draw_decks()
        self._draw_top_info()
        self._draw_bottom_info()
        self._draw_ability_button()
