import numpy as np
import cv2
import sys


SCX, SCY = 700, 700
image = 255 * np.ones((SCX, SCY, 4), np.uint8)
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



def heuristic(p1, p2):
    # heuristic value, change it for less accurate but faster result
    return (abs((p1[0] - p2[0]))) + (abs((p1[1] - p2[1])))


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


def change_color_bright(color, factor=0):
    # this function will change the brightness of the color
    # if the factor > 0, it will be lighter, else, darker.
    b = np.clip(color[0] + factor, 0, 255)
    g = np.clip(color[1] + factor, 0, 255)
    r = np.clip(color[2] + factor, 0, 255)
    a = 1
    return [int(b), int(g), int(r), int(a)]


def print_maze(maze, open_list, closed_list, start, end):
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
    for node in open_list:
        y = node.position[0]
        x = node.position[1]
        draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, GREY)
    for node in closed_list:
        y = node.position[0]
        x = node.position[1]
        color = GREEN.copy()
        color[2] = heuristic(node.position, end) * (1 * 200 / leny)
        draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, color)
    y = start[0]
    x = start[1]
    draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, SKYBLUE_FLASH)
    y = end[0]
    x = end[1]
    draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, PURPLE)
    cv2.imshow('Astar Visualizer', image)
    cv2.waitKey(1)

def draw_path(start, end, maze, path):
    leny = len(maze)
    lenx = len(maze[0])
    wy = SCY / leny
    wx = SCX / lenx
    for pos in path:
        y = pos[0]
        x = pos[1]
        draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, PINK)
    y = start[0]
    x = start[1]
    draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, SKYBLUE_FLASH)
    y = end[0]
    x = end[1]
    draw_rect(x * wx, y * wy, x * wx + wx, y * wy + wy, PURPLE)
    cv2.imshow('Astar Visualizer', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
