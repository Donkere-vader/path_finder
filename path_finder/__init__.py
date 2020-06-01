import main
import sys

__version__ = "0.0.1"

if len(sys.argv) <= 1:
    print('Please provide a maze script, view the README for more info.')
    exit()

maze_name = sys.argv[1]

if __name__ == "__main__":
    main.main(maze_name)