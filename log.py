import stddraw


class Log:
    def __init__(self):
        # TODO: adapt stddraw to be an object with its own window instance
        stddraw.setCanvasSize(500, 750)
        stddraw.setXscale(0, 500)
        stddraw.setYscale(0, 750)

    def update(self):
        stddraw.show()
