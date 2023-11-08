import stddraw


class Gui:
    WIDTH, HEIGHT = 1000, 750
    PADDING = 25

    # top info bar
    INFO_TOP_W = 400
    INFO_TOP_H = 50
    INFO_TOP_L, INFO_TOP_R = WIDTH // 2 - INFO_TOP_W // 2, WIDTH // 2 + INFO_TOP_W // 2
    INFO_TOP_T = HEIGHT
    INFO_TOP_B = INFO_TOP_T - INFO_TOP_H
    # bottom info bar
    INFO_BOT_W = WIDTH - 2 * PADDING
    INFO_BOT_H = 100
    INFO_BOT_L, INFO_BOT_R = PADDING, WIDTH - PADDING
    INFO_BOT_T, INFO_BOT_B = INFO_BOT_H, 0

    # player 1 deck positions
    DECK_1_L, DECK_1_R = PADDING, WIDTH // 2 - PADDING // 2
    DECK_1_T, DECK_1_B = INFO_TOP_B - PADDING, INFO_BOT_T + PADDING
    DECK_1_W = DECK_1_R - DECK_1_L
    DECK_1_H = DECK_1_T - DECK_1_B
    # player 2 deck positions
    DECK_2_L, DECK_2_R = WIDTH // 2 + PADDING, WIDTH - PADDING
    DECK_2_T, DECK_2_B = INFO_TOP_B - PADDING, INFO_BOT_T + PADDING
    DECK_2_W = DECK_2_R - DECK_2_L
    DECK_2_H = DECK_2_T - DECK_2_B

    @staticmethod
    def draw_filled_rect(x, y, w, h, fill_color=stddraw.LIGHT_GRAY):
        stddraw.setPenColor(fill_color)
        stddraw.filledRectangle(x, y, w, h)
        stddraw.setPenColor()
        stddraw.rectangle(x, y, w, h)

    def __init__(self, game_state, w=1000, h=750):
        stddraw.setCanvasSize(w, h)
        stddraw.setXscale(0, w)
        stddraw.setYscale(0, h)
        self.game = game_state

    def _draw_top_info(self):
        Gui.draw_filled_rect(
            self.INFO_TOP_L, self.INFO_TOP_B, self.INFO_TOP_W, self.INFO_TOP_H
        )

    def _draw_bottom_info(self):
        Gui.draw_filled_rect(
            self.INFO_BOT_L, self.INFO_BOT_B, self.INFO_BOT_W, self.INFO_BOT_H
        )

    def draw_card(self, x, y):
        pass

    def _draw_decks(self):
        # draw player 1 deck
        Gui.draw_filled_rect(self.DECK_1_L, self.DECK_1_B, self.DECK_1_W, self.DECK_1_H)

        # draw player 2 deck
        Gui.draw_filled_rect(self.DECK_2_L, self.DECK_2_B, self.DECK_2_W, self.DECK_2_H)

    def update(self):
        self._draw_decks()
        self._draw_top_info()
        self._draw_bottom_info()
        stddraw.show()
        pass
