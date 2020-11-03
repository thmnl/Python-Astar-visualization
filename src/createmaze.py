import numpy as np
import cv2
import sys

SCX, SCY = 700, 700
image = 255 * np.ones((SCX, SCY, 4), np.uint8)
start = None
end = None
down = False
maze = None
draw = True
SKYBLUE = [250, 206, 135, 1]
SKYBLUE_FLASH = [255, 255, 0, 1]
PURPLE_BLUE = [240, 144, 141, 1]
GREY_BLUE = [162, 161, 130, 1]
YELLOW = [79, 243, 241, 1]
YELLOW_FLASH = [0, 255, 255, 1]
PINK = [249, 99, 233, 1]
PURPLE = [157, 40, 145, 1]
ORANGE = [40, 153, 242, 1]
LIGHT_BROWN = [141, 196, 240, 1]
RED = [100, 100, 255, 1]
SCARLET_RED = [24, 24, 165, 1]
BROWN = [65, 103, 155, 1]
GREEN = [100, 255, 100, 1]
GREEN_CLEAR = [141, 240, 185, 1]
DARK_GREEN = [20, 150, 20, 1]
GREY = [75, 75, 75, 1]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]


def draw_rect(x1, y1, x2, y2, color):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    pt1 = (x1, y1)
    pt2 = (x1, y2)
    pt3 = (x2, y2)
    pt4 = (x2, y1)
    pts = np.array([pt1, pt2, pt3, pt4], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(image, [pts], color)
    cv2.polylines(image, [pts], True, BLACK)


def print_maze(maze, start, end):
    global draw

    leny = len(maze)
    lenx = len(maze[0])
    wy = SCY / leny
    wx = SCX / lenx
    for y, mazey in enumerate(maze):
        for x, value in enumerate(mazey):
            color = BLACK
            if value:
                color = WHITE
            draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, color)
    if start:
        y = start[0]
        x = start[1]
        draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, SKYBLUE_FLASH)
    if end:
        y = end[0]
        x = end[1]
        draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, PURPLE)
    cv2.imshow('Astar Visualizer', image)
    key = cv2.waitKey(1)
    if key == 32: #space bar
        draw = False


def get_pos(x, y, maze):
    leny = len(maze)
    lenx = len(maze[0])
    wy = SCY / leny
    wx = SCX / lenx
    return (int(y / wy), int(x / wx))


def create_maze(args):
    global start, end, down, maze

    x, y = 30, 30
    if args.maze_size:
        if len(args.maze_size) == 1:
            x, y = args.maze_size[0], args.maze_size[0]
        else:
            x, y = args.maze_size[0], args.maze_size[1]
    maze = np.random.choice([1], size=(x, y), p=[3 / 3])


def mouse_callback(event, x, y, flags, param):
    global start, end, down, maze

    if event == 1 or down: #mouse down
        down = True
        pos = get_pos(x, y, maze)
        if not start and event == 1:
            start = pos
        elif not end and event == 1:
            end = pos
        else:
            try:
                if end and start and pos != end and pos != start:
                    maze[pos[0]][pos[1]] = 0
            except IndexError:
                pass
    if event == 4: #mouse up
        down = False

def main(args):
    global maze, start, end, draw

    cv2.namedWindow("Astar Visualizer")
    cv2.setMouseCallback("Astar Visualizer", mouse_callback)
    create_maze(args)
    while draw:
        print_maze(maze, start, end)
    return {"maze": maze, "start": start, "end": end}
