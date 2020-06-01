
class Node:
    def __init__(self, x, y):
        self.distance = "infinity"
        self.via = False
        self.x = x
        self.y = y
        self.neighbours = []


    def __repr__(self):
        return f"<Node object pos: ({self.x}, {self.y})>"