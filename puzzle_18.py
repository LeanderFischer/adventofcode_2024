#! /usr/bin/python3

from typing import List, Tuple, Dict

import re
import numpy as np

from heapq import heappush, heappop

infile: str = "./puzzle_18_input.txt"

f = open(infile, "r")

data: List[str] = f.read().split('\n')

# print(f'{data = }')
# print(f'{data[0] = }')

directions: List[List[int]] = [
    [0, 1],
    [-1, 0],
    [0, -1],
    [1, 0],
]

def find_shortest_path_bfs(
    grid: np.ndarray,
) -> int:

    # set start/end points
    start: List[int] = [0, 0]
    end: List[int] = [len(grid) - 1, len(grid[0]) - 1]

    # define priority queue
    priority_queue: List[Tuple(int, List[int])] = []  # steps, position

    # add starting point
    heappush(priority_queue, (0, start))

    # define visited set
    visited: set = set()
    visited.add(tuple(start))

    while priority_queue:
        steps, position = heappop(priority_queue)

        # print(f'{position = }')
        # print(f'{end = }')

        # check whether we reached the end
        if position == end:
            return steps

        # otherwise check in all 4 directions
        for take_step in directions:
            new_position = [ position[0] + take_step[0], position[1] + take_step[1] ]

            # print(f'Checking position {new_position = }')

            # check whether this position is valid
            if new_position[0] < 0 or new_position[0] > len(grid) - 1 or new_position[1] < 0 or new_position[1] > len(grid[0]) - 1 or tuple(new_position) in visited:
                continue

            # print(f'Checking position {new_position = }')

            if grid[new_position[0], new_position[1]] == '#':
                continue

            # print(f'Adding this position to priority queue: {new_position = }')
            heappush(priority_queue, (steps+1, new_position))
            visited.add(tuple(new_position))

        # print(f'{priority_queue = }')

    # in case none is found, return infinite
    return np.inf


# create 2-D grid of memory (70x70)
# test grid
# range_x: int = 7
range_x: int = 71
range_y: int = range_x

grid: np.ndarray = np.array( [ np.array( ['.' for i in range(range_x)] ) for j in range(range_x)] )
# print(f'{grid = }')
# print(f'{grid[0,1] = }')


# PART 1

# # loop through the input data and mark corrupet memory in the grid
# for count, memory in enumerate(data):
#     # print(f'{count = }')
#     # print(f'{memory = }')
#     # get and y coordinates
#     position: List[int] = [ int(value) for value in re.findall('\d+', memory) ]
#     # print(f'{position = }')
#     # mark as corrupted in grid
#     grid[position[1], position[0]] = '#'

#     # test grid
#     # if count == 11:
#     if count == 1023:
#         break

# # print(f'{grid = }')

# shortest_path = find_shortest_path_bfs(grid)
# print(f'{shortest_path = }')


# PART 2

# loop through the input data and mark corrupet memory in the grid
for count, memory in enumerate(data):
    # print(f'{count = }')
    # print(f'{memory = }')
    # get and y coordinates
    position: List[int] = [ int(value) for value in re.findall('\d+', memory) ]
    # print(f'{position = }')
    # mark as corrupted in grid
    grid[position[1], position[0]] = '#'

    if find_shortest_path_bfs(grid) == np.inf:
        print(f'{position = }')
        print(f'{count = }')
        break

# print(f'{grid = }')
