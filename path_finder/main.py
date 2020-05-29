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


def main(maze_name):
    global path_finder
    path_finder = PathFinder(maze_name)
    arcade.run()