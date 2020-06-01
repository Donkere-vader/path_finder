import sys

class MazeTiles:
    def __init__(self):
        self.air = "air"
        self.wall = "wall"
        self.start = "start"
        self.end = "end"

class MazeHandler:
    def __init__(self):
        pass

    def load_maze(self, maze_name):
        maze_tiles = MazeTiles()

        _maze_file = [l.replace('\n', '') for l in open(maze_name, 'r').readlines()]
        _maze = []

        for line in _maze_file:
            if not line:
                continue
            _maze_line = []

            for c in line:
                if c == "#":
                    _maze_line.append(maze_tiles.wall)
                elif c.upper() == "S":
                    _maze_line.append(maze_tiles.start)
                elif c.upper() == "E":
                    _maze_line.append(maze_tiles.end)
                else:
                    _maze_line.append(maze_tiles.air)

            _maze.append(
                    _maze_line
            )

        return _maze