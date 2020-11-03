import sys
import numpy as np
import cv2
import time
import src.mazes as mazes
import src.draw as draw
import src.createmaze as createmaze
from src.ft_argparse import get_args
import json


args = None


class Node:
    """
        (tuple) position [0] = x, [1] = y
        (int) g represent the cost, (int) f the result of cost + heuristic
        (Node) parent is the parent node
    """

    def __init__(self, position, f=0, g=0):
        self.position = position
        self.f, self.g = f, g
        self.parent = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return list(self.position) == list(other.position)


def heuristic(p1, p2):
    # heuristic value, change it for less accurate but faster result
    return (abs((p1[0] - p2[0]))) + (abs((p1[1] - p2[1])))


def neighbors(current_node, maze):
    """
        return every valid neighbors of a current_node in the maze
    """
    UP, DOWN, LEFT, RIGHT = -1, 1, -1, 1
    neighbors = []
    pos = [(0, UP), (0, DOWN), (LEFT, 0), (RIGHT, 0)]
    diag = [(LEFT, UP), (RIGHT, DOWN), (LEFT, DOWN), (RIGHT, UP)]
    if not args.disable_diagonal:
        pos += diag
    for new_position in pos:
        node_position = (
            current_node.position[0] + new_position[0],
            current_node.position[1] + new_position[1],
        )            
        # range check
        if (
            node_position[0] > (len(maze) - 1)
            or node_position[0] < 0
            or node_position[1] > (len(maze[node_position[0]]) - 1)
            or node_position[1] < 0
        ):
            continue
        # wall check
        if new_position in diag:
            if (
                    maze[current_node.position[0]][current_node.position[1] + new_position[1]] == 0 
                    and maze[current_node.position[0] + new_position[0]][current_node.position[1]] == 0
                ):
                continue
        if maze[node_position[0]][node_position[1]] == 0:
            continue
        new_node = Node(node_position)
        # g is how the cost of the step
        if new_position[0] != 0 and new_position[1] != 0:
            new_node.g = current_node.g + 1.44
        else:
            new_node.g = current_node.g + 1
        new_node.parent = current_node
        neighbors.append(new_node)
    return neighbors


def construct_path(node):
    """
        return the path from the given node to his farthest parent
    """
    path = []
    current = node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path


def shortest_path(start, end, maze, display=True):
    # A* algorithm : https://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html
    # create start and end nodes
    start_node = Node(start)
    end_node = Node(end)
    start_node.g = 0
    start_node.f = start_node.g + heuristic(start, end)
    # init open and c.losed list
    open_list = [start_node]
    closed_list = []
    while len(open_list) > 0:
        t = time.time()
        open_list.sort(key=lambda x: x.f)
        current_node = open_list[0]
        if current_node == end_node:
            path = construct_path(current_node)
            # construct_path return from end to start, reverse it.
            path.reverse()
            return path
        open_list.remove(current_node)
        closed_list.append(current_node)
        for neighbor in neighbors(current_node, maze):
            # check if the potential new node is in the closed_list and ignore it if that's the case
            if neighbor in closed_list:
                continue
            # calculate f, the queue priority depend on f, so the final result depend of the heuristic formula
            # more the formula is "unprecise", less time it takes to calculate, but the result may change to a less accurate path
            neighbor.f = neighbor.g + heuristic(neighbor.position, end)
            # check if the potential new node is in the opened_list and if that's the case,
            # if the cost (g) is greater for the opened node, change his value.
            for opened in open_list:
                if neighbor.position == opened.position:
                    if neighbor.g < opened.g:
                        opened.g = neighbor.g
                        opened.parent = neighbor.parent
                    break
            if neighbor not in open_list:
                open_list.append(neighbor)
        if display:
            draw.print_maze(maze, open_list, closed_list, start, end)
    return None



def dct_init():
    if len(args.mazefile):
        with open(args.mazefile[0]) as f:
            dct = json.load(f)
    elif (args.random_maze):
        path = None
        while not path:
            try:
                dct = mazes.generate_random_maze(args)
            except UnboundLocalError:
                continue
            dct["display"] = False
            path = shortest_path(**dct)
        dct.pop("display", False)
    else:
        dct = createmaze.main(args)
    return dct


def save_maze(dct):
    if not args.save_maze:
        return
    if not args.output:
        filename = "maze" + str(time.time()).split('.')[0] + ".json"
    else:
        filename = args.output
    dct["maze"] = dct["maze"].tolist()
    with open(filename, 'w') as outfile:
        json.dump(dct, outfile)
    

def main():
    global args
    args = get_args()
    dct = dct_init()
    save_maze(dct)
    dct["path"] = shortest_path(**dct)

    if not dct["path"]:
        print("no path")
        time.sleep(3)
        return
        
    draw.draw_path(**dct)



if __name__ == "__main__":
    main()
