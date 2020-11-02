import numpy as np
import cv2
import sdl2.ext
import sys

SCX, SCY = 700, 700
window = None
windowArray = None
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


def init():
    global window
    global windowArray

    sdl2.ext.init()
    window = sdl2.ext.Window("Astar Visualizer", size=(SCX, SCY))
    windowArray = sdl2.ext.pixels3d(window.get_surface())
    window.show()


def get_events():
    events = sdl2.ext.get_events()
    for e in events:
        if e.type == sdl2.SDL_QUIT:
            sdl2.ext.quit()
            sys.exit(0)
            break


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
    get_events()
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
    np.copyto(windowArray, image.swapaxes(0, 1))
    window.refresh()


def get_pos(x, y, maze):
    leny = len(maze)
    lenx = len(maze[0])
    wy = SCY / leny
    wx = SCX / lenx
    return (int(y / wy), int(x / wx))


def create_maze(args):
    x, y = 30, 30
    if args.maze_size:
        if len(args.maze_size) == 1:
            x, y = args.maze_size[0], args.maze_size[0]
        else:
            x, y = args.maze_size[0], args.maze_size[1]
    maze = random_maze = np.random.choice([1], size=(x, y), p=[3 / 3])
    start = None
    end = None
    down = False
    while True:
        events = sdl2.ext.get_events()
        for e in events:
            if e.type == sdl2.SDL_QUIT:
                sdl2.ext.quit()
                sys.exit(0)
                break
            if e.type == sdl2.SDL_KEYDOWN:
                if e.key.keysym.sym == 27:  # ESC
                    sdl2.ext.quit()
                    break
                if e.key.keysym.sym == ord(" "):
                    sdl2.ext.quit()
                    return {"maze": maze, "start": start, "end": end}
            if e.type == sdl2.SDL_MOUSEBUTTONDOWN or down:
                pos = get_pos(e.button.x, e.button.y, maze)
                if not start:
                    start = pos
                    continue
                if not end:
                    end = pos
                    continue
                try:
                    maze[pos[0]][pos[1]] = 0
                except IndexError:
                    pass

                down = True
            if e.type == sdl2.SDL_MOUSEBUTTONUP:
                down = False
        print_maze(maze, start, end)


def main(args):
    init()
    return create_maze(args)
