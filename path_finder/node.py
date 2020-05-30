
class Node:
    def __init__(self, x, y, parent):
        self.distance = "infinity"
        self.via = None
        self.x = x
        self.y = y
        self.neighbours = [parent]