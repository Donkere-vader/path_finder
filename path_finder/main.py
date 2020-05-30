import arcade
from maze_handler import MazeHandler, MazeTiles
from config import FULL_SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE
from node import Node

""" Path finding program that uses arcade to visualize it """

class PathFinder(arcade.Window):
    def __init__(self, maze_name):
        _screen_title = f"{SCREEN_TITLE} - {maze_name}"
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, _screen_title, fullscreen=FULL_SCREEN)
        self.maze_name = maze_name
        self.maze_handler = MazeHandler()
        self.maze = self.maze_handler.load_maze(self.maze_name)

        self.maze_tiles = MazeTiles()
        self.box_width = SCREEN_WIDTH / len(self.maze[0])
        self.box_height = SCREEN_HEIGHT / len(self.maze)

        self.start()

    def start(self):
        """ Start finding some paths """

        # get nodes
        self.nodes = [] # all the junctions

        self.start = False
        self.end = False

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == self.maze_tiles.start:
                    self.start = (x, y)
                elif self.maze[y][x] == self.maze_tiles.end:
                    self.end = (x, y)

        if not self.start or not self.end:
            print('ERROR: Provide an start and end point in the maze') # TODO propper error's
            exit()

        #self.get_nodes(self.start[0], self.start[1])

    
    #def get_nodes(self, x: int, y: int):
        
        self.checked_squares = []
        self.check_square(self.start[0], self.start[1])

        """        _text_maze = []

        for line in self.maze:
            _line = []
            for tile in line:
                _c = " "
                if tile == self.maze_tiles.start:
                    _c = "S"
                elif tile == self.maze_tiles.end:
                    _c = "E"
                elif tile == self.maze_tiles.wall:
                    _c = "#"
                _line.append(_c)
            _text_maze.append(
                _line
            )
        
        for line in _text_maze:
            print()
            for c in line:
                print(c, end="")
        
        for node in self.nodes:
            print(node.x, node.y)
            _text_maze[node.y][node.x] = "N"
        

        for line in _text_maze:
            print()
            for c in line:
                print(c, end="")

        print()"""

    def check_square(self, x, y):
        self.checked_squares.append((x, y))
        if self.maze[y][x] != self.maze_tiles.air and self.maze[y][x] != self.maze_tiles.start:
            return False

        # check surrounding squares
        surrounding_air = []

        for _x, _y in zip([0, 0, -1, 1], [-1, 1, 0, 0]):
            if not (y + _y >= 0 or y + _y <= len(self.maze)) or not(x + _x >=0 or x + _x <= len(self.maze[y])):
                continue

            print(_x, _y)
            if self.maze[y + _y][x + _x] == self.maze_tiles.air:
                surrounding_air.append((x + _x, y + _y))

            if (x + _x, y + _y) not in self.checked_squares:
                self.check_square(x + _x, y + _y)
    
        add = True
        print(f"({x}, {y}) SURROUNDING AIR: {surrounding_air}")
        if len(surrounding_air) == 2 and (surrounding_air[0][0] == surrounding_air[1][0] or surrounding_air[0][1] == surrounding_air[1][1]):
            add = False

        if add:
            if len(self.nodes) == 0:
                neighbour = None
            else:
                neighbour = self.nodes[-1]
            self.nodes.append(
                Node(
                    x + _x - 1,
                    y + _y,
                    neighbour
                )
            )
    

        # return true because je suis air
        return True

    def on_draw(self):
        arcade.start_render()

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == self.maze_tiles.wall:
                    color = (255, 255, 255)
                elif self.maze[y][x] == self.maze_tiles.start:
                    color = (0, 255, 0)
                elif self.maze[y][x] == self.maze_tiles.end:
                    color = (255, 0, 0)
                else:
                    # is air thus dont draws
                    continue

                arcade.draw_rectangle_filled(
                    x * self.box_width + self.box_width / 2,
                    SCREEN_HEIGHT - (y * self.box_height + self.box_height / 2),
                    self.box_width,
                    self.box_height,
                    color
                )
        
        for node in self.nodes:
            try:
                arcade.draw_text(
                    text=f"({node.x}, {node.y})", 
                    start_x=(node.x) * self.box_width + self.box_width / 2,
                    start_y=SCREEN_HEIGHT - (node.y * self.box_height + self.box_height / 2),
                    color=(250, 0, 250)
                )
            except:
                import sys
                print(sys.exc_info())
            arcade.draw_circle_filled(
                (node.x) * self.box_width + self.box_width / 2,
                SCREEN_HEIGHT - (node.y * self.box_height + self.box_height / 2),
                4,
                (200, 200, 200)
            )


def main(maze_name):
    global path_finder
    path_finder = PathFinder(maze_name)
    arcade.run()