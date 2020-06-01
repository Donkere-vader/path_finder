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

        self.setup()

    def setup(self):
        """ Generate the nodes and put it all in lists and stuff """

        # get nodes
        self.nodes = [[None for i in range(len(self.maze[0]))] for i in range(len(self.maze))] # all the junctions

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
        
        self.checked_tiles = []
        self.check_tile(self.start[0], self.start[1])

        # give all the nodes their neigbours
        for y in self.nodes:
            for node in y:
                if node:
                    for x, y in zip([1, -1, 0, 0], [0, 0, 1, -1]):
                        i = 1
                        print(f"{node} | Looking at: ({node.x + x * i}, {node.y + y * i})")
                        if node.y + y * i >= len(self.maze) or node.y + y * i < 0 or node.x + x * i >= len(self.maze[0]) or node.x + x * i < 0:
                            continue


                        while self.maze[node.y + y * i][node.x + x * i] == self.maze_tiles.air or self.maze[node.y + y * i][node.x + x * i] == self.maze_tiles.end:
                            if self.nodes[node.y + y * i][node.x + x * i]:
                                node.neighbours.append(self.nodes[node.y + y * i][node.x + x * i])
                                break
                            
                            i += 1

        print("==> nodes <==")
        for y in self.nodes:
            for node in y:
                if node:
                    print(node)
                    print(f"\tNeigbours: {node.neighbours}")

        self.checked_nodes = []
        self.find_path()

    def find_path(self):
        self.path = []

        for y in self.nodes:
            for node in y:
                if node:
                    if self.maze[node.y][node.x] == self.maze_tiles.start:
                        _start_node = node
                        break

        _start_node.distance = 0
        print("\n\n=== CHECKING NODES ===")
        self.check_node(_start_node)


    def check_node(self, node):
        print(f"Checking {node}")
        try:   
            self.checked_nodes.append(node)
            for neighbour in node.neighbours:
                distance = abs(node.x - neighbour.x) + abs(node.y - neighbour.y)
                if neighbour.distance == "infinity" or neighbour.distance > node.distance + distance:
                    neighbour.distance = node.distance + distance
                    neighbour.via = node

                if self.maze[neighbour.y][neighbour.x] == self.maze_tiles.end:
                    self.append_path(neighbour)
                    print(" < == PATH FOUND == >")
                    _text_path = []

                    for n in self.path:
                        if n.via:
                            print(f"{n} ({n.x}, {n.y}) Distance: {n.distance} | Via: ({n.via.x}, {n.via.y})")
                        else:
                            print(f"{n} ({n.x}, {n.y}) Distance: {n.distance} | Via: ({n.via})")



                elif neighbour not in self.checked_nodes:
                    self.check_node(neighbour)
        except:
            import sys
            print(sys.exc_info())

    def append_path(self, node):
        self.path.append(node)

        if node.via:
            self.append_path(node.via)

    def check_tile(self, x, y):
        self.checked_tiles.append((x, y))
        if (self.maze[y][x] != self.maze_tiles.air and self.maze[y][x] != self.maze_tiles.end and self.maze[y][x] != self.maze_tiles.start) or x < 0 or y < 0:
            return False

        # check surrounding tiles
        surrounding_air = []

        for _x, _y in zip([0, 0, -1, 1], [-1, 1, 0, 0]):
            if y + _y < 0 or y + _y >= len(self.maze) or x + _x < 0 or x + _x >= len(self.maze[y]):
                continue

            if self.maze[y + _y][x + _x] == self.maze_tiles.air:
                surrounding_air.append((x + _x, y + _y))

            if (x + _x, y + _y) not in self.checked_tiles:
                self.check_tile(x + _x, y + _y)
    
        add = True
        if len(surrounding_air) == 2 and (surrounding_air[0][0] == surrounding_air[1][0] or surrounding_air[0][1] == surrounding_air[1][1]):
            add = False

        if add:
            self.nodes[y][x] = Node(
                    x + _x - 1,
                    y + _y,
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
        
        for n in self.path:
            arcade.draw_circle_filled(
                n.x * self.box_width + self.box_width / 2,
                SCREEN_HEIGHT - (n.y * self.box_height + self.box_height /2),
                5,
                (255, 0, 0)
            )


def main(maze_name):
    global path_finder
    path_finder = PathFinder(maze_name)
    arcade.run()