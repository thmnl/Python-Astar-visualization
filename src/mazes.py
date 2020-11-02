import numpy as np
import random

def generate_random_maze(args):
    if args.maze_size and len(args.maze_size) == 1:
        rx = args.maze_size[0]
        ry = rx
    elif args.maze_size and len(args.maze_size) > 1:
        rx = args.maze_size[0]
        ry = args.maze_size[1]
    else:
        rx = random.randint(15, 55)
        ry = rx
    random_maze = np.random.choice([0, 1], size=(rx, ry), p=[1.5 / 3, 1.5 / 3])
    for i, x in enumerate(random_maze[0]):
        if x == 1:
            start = (0, i)
            break
    for i, x in enumerate(random_maze[-1]):
        if x == 1:
            end = (ry - 1, i)
    return {"maze": random_maze, "start": start, "end": end}
