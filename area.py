class Area:
    def __init__(self, left, right, bottom, top):
        self.x = range(left, right)
        self.y = range(bottom, top)

    def is_clicked(self, x, y):
        return x in self.x and y in self.y
