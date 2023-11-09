import stddraw_oop as stddraw
import picture
from game import Game


class Gui:
    WIDTH, HEIGHT = 1000, 750
    PADDING = 25

    # LOG_W = 300
    # LOG_R = WIDTH - PADDING
    # LOG_L = LOG_R - LOG_W
    # LOG_T, LOG_B = HEIGHT - PADDING, PADDING
    # LOG_H = LOG_T - LOG_B
    # MAIN_R = LOG_L - PADDING
    MAIN_R = WIDTH

    # top info bar
    INFO_TOP_W = 400
    INFO_TOP_H = 50
    INFO_TOP_L, INFO_TOP_R = (
        MAIN_R // 2 - INFO_TOP_W // 2,
        MAIN_R // 2 + INFO_TOP_W // 2,
    )
    INFO_TOP_T = HEIGHT
    INFO_TOP_B = INFO_TOP_T - INFO_TOP_H
    # bottom info bar
    INFO_BOT_W = MAIN_R - 2 * PADDING - 100
    INFO_BOT_H = 100
    INFO_BOT_L, INFO_BOT_R = PADDING, MAIN_R - PADDING
    INFO_BOT_T, INFO_BOT_B = INFO_BOT_H, 0

    # player 1 deck positions
    DECK_1_L, DECK_1_R = PADDING, MAIN_R // 2 - PADDING
    DECK_1_T, DECK_1_B = INFO_TOP_B - PADDING, INFO_BOT_T + PADDING
    DECK_1_W = DECK_1_R - DECK_1_L
    DECK_1_H = DECK_1_T - DECK_1_B
    # player 2 deck positions
    DECK_2_L, DECK_2_R = MAIN_R // 2 + PADDING, MAIN_R - PADDING
    DECK_2_T, DECK_2_B = INFO_TOP_B - PADDING, INFO_BOT_T + PADDING
    DECK_2_W = DECK_2_R - DECK_2_L
    DECK_2_H = DECK_2_T - DECK_2_B
    # cards
    CARD_W = DECK_1_W // 2
    CARD_H = DECK_1_H // 3

    MOUSE_LEFT = True
    MOUSE_RIGHT = False

    PLAYER_COLORS = {True: stddraw.BOOK_RED, False: stddraw.BOOK_BLUE}

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
          "deck_1":  Area("deck_1", self.DECK_1_L, self.DECK_1_R, self.DECK_1_B, self.DECK_1_T),
          "deck_2":  Area("deck_2", self.DECK_2_L, self.DECK_2_R, self.DECK_2_B, self.DECK_2_T),
          "ability":  Area("ability", self.DECK_1_L, self.DECK_1_R, self.DECK_1_B, self.DECK_1_T),
        }  # fmt:on

    def _draw_log(self):
        # Gui.draw_filled_rect(self.LOG_L, self.LOG_B, self.LOG_W, self.LOG_H)
        pass

    def _draw_top_info(self):
        Gui.draw_filled_rect(
            self.INFO_TOP_L, self.INFO_TOP_B, self.INFO_TOP_W, self.INFO_TOP_H
        )

        curr_player = self.game.get_player()
        player_text = f"Player {int(curr_player) + 1}"
        round_text = f"Round {self.game.get_round()}"
        x_1 = self.INFO_TOP_L + self.INFO_TOP_W // 4
        x_2 = self.INFO_TOP_L + (3 * self.INFO_TOP_W // 4)
        y = self.INFO_TOP_B + self.INFO_TOP_H // 2
        stddraw.text(x_1, y, round_text)
        stddraw.setPenColor(self.PLAYER_COLORS[curr_player])
        stddraw.text(x_2, y, player_text)
        stddraw.setPenColor()

    def _draw_bottom_info(self):
        Gui.draw_filled_rect(
            self.INFO_BOT_L, self.INFO_BOT_B, self.INFO_BOT_W, self.INFO_BOT_H
        )

    def _draw_card(self, left, bottom, side):
        center_x = left + self.CARD_W // 2
        center_y = bottom + self.CARD_H // 2
        color = self.PLAYER_COLORS[side]
        stddraw.setPenColor(color)
        stddraw.filledCircle(center_x, center_y, self.CARD_W // 4)
        stddraw.setPenColor()

    def _draw_deck_grid(self, left, side):
        stddraw.setPenRadius(1.5)

        # draw the middle line
        stddraw.line(
            left + self.CARD_W, self.DECK_1_T, left + self.CARD_W, self.DECK_1_B
        )

        # draw the lines and the cards for each of the 3 rows
        for row in range(self.DECK_1_B, self.DECK_1_T - self.CARD_H // 2, self.CARD_H):
            if row > self.DECK_1_B and row < self.DECK_1_T - 1:
                stddraw.line(left + 1, row, left + self.DECK_1_W, row)

            # for now each card is a circle
            self._draw_card(left, row, side)  # left col
            self._draw_card(left + self.CARD_W, row, side)  # right col

        stddraw.setPenRadius()

    def _draw_decks(self):
        # draw player 1 deck
        Gui.draw_filled_rect(self.DECK_1_L, self.DECK_1_B, self.DECK_1_W, self.DECK_1_H)
        self._draw_deck_grid(self.DECK_1_L, False)

        # draw player 2 deck
        Gui.draw_filled_rect(self.DECK_2_L, self.DECK_2_B, self.DECK_2_W, self.DECK_2_H)
        self._draw_deck_grid(self.DECK_2_L, True)

    def get_mouse_click(self):
        while True:
            stddraw.show(100)
            if stddraw.mousePressed():
                side = stddraw.mouseSide()
                return side == "left", stddraw.mousePos()

    def get_index(self):
        side, pos = self.get_mouse_click()
        while not (side == Gui.MOUSE_LEFT):
            if side == Gui.MOUSE_RIGHT:
                print("clicked info of something")
            side, pos = self.get_mouse_click()

        # we know side == MOUSE_LEFT
        # check if pos is in DECK_AREA
        # if it is, get the object's information
        print("clicked a card")

    def update(self):
        self._draw_log()
        self._draw_decks()
        self._draw_top_info()
        self._draw_bottom_info()
        pass


class Area:
    def __init__(self, name, left, right, bottom, top):
        self.name = name
        self.x = range(left, right)
        self.y = range(bottom, top)

    def is_clicked(self, x, y):
        return x in self.x and y in self.y

    def in_area(self, x, y, area_name):
        return self.is_clicked(x, y) and self.name == area_name
