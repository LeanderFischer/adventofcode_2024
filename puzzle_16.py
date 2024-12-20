#! /usr/bin/python3

import time
t0 = time.time()

# print(f'Starting at time {t0} ...')

import sys
sys.setrecursionlimit(10000)

from typing import List, Tuple, Dict

# from collections import deque
from heapq import heappush, heappop

import numpy as np

import copy

infile: str = "./puzzle_16_input.txt"

f = open(infile, "r")

data: List[List[str]] = [ [ char for char in string ] for string in f.read().split('\n') ]

# print(f'{data = }')
# print(f'{data[0] = }')


def find_start(data: List[List[str]]) -> List[int]:
    start: List[int] = list()
    for i in reversed(range(len(data))):
        for j in range(len(data[0])):
            if data[i][j] == 'S':
                start = [i, j]
    return start


def find_finish(data: List[List[str]]) -> List[int]:
    finish: List[int] = list()
    for i in range(len(data)):
        for j in reversed(range(len(data[0]))):
            if data[i][j] == 'E':
                finish = [i, j]
    return finish

directions: List[List[int]] = [
    [0, 1],
    [-1, 0],
    [0, -1],
    [1, 0],
]


# def find_possible_paths_DFS(
#     data: List[List[str]],
#     position: List[int],
#     score: int,
#     direction: int,
#     visited: set = set(),
#     # steps: List[int] = [],
# # ) -> Tuple[int, List[int]]:
# ) -> int:

#     this_position: List[int] = [ position[0] + directions[direction][0], position[1] + directions[direction][1] ]

#     # print(f'Checking position {this_position = } coming from {position = }')

#     # if we reached a wall or already visited spot, return infinite value
#     if data[this_position[0]][this_position[1]] in ['#', 'X'] or tuple(this_position) in visited:
#         return np.inf
#         # return np.inf, steps

#     # we reached the end, return the score
#     if data[this_position[0]][this_position[1]] in ['E']:
#         return score
#         # return score, steps + [direction]

#     # # make a deep copy of the data to avoid shared state issues
#     # new_data = copy.deepcopy(data)
#     # new_data[this_position[0]][this_position[1]] = 'X'  # Mark as visited

#     # print(f'Checking directions {direction = }, {(direction + 1) % 4 = }, and {(direction + 3) % 4 = }')

#     visited.add(tuple(this_position))

#     # straight: Tuple[int, List[int]] = find_possible_paths_DFS(
#     straight: int = find_possible_paths_DFS(
#         data = data,
#         # data = new_data,
#         position = this_position,
#         score = score + 1,
#         direction = direction,
#         visited = visited.copy(),
#         # steps = steps + [direction],
#     )

#     # left: Tuple[int, List[int]] = find_possible_paths_DFS(
#     left: int = find_possible_paths_DFS(
#         data = data,
#         # data = new_data,
#         position = this_position,
#         score = score + 1001,
#         direction = (direction + 1) % 4,
#         visited = visited.copy(),
#         # steps = steps + [(direction + 1) % 4],
#     )

#     # right: Tuple[int, List[int]] = find_possible_paths_DFS(
#     right: int = find_possible_paths_DFS(
#         data = data,
#         # data = new_data,
#         position = this_position,
#         score = score + 1001,
#         direction = (direction + 3) % 4,
#         visited = visited.copy(),
#         # steps = steps + [(direction + 3) % 4],
#     )

#     # scores: List[Tuple[int, List[int]]] = sorted( [straight, left, right], key=lambda x:x[0])
#     scores: List[int] = sorted( [straight, left, right])
#     # print(f'{scores = }')

#     return scores[0]


# BFS solution:

def find_possible_paths_BFS(
    data: List[List[str]],
    start: List[int],
    score: int,
) -> int:

    visited: set = set()
    visited.add(tuple(start))

    priority_queue: List[Tuple[int, List[int], int, int, List[int]]] = []  # (score, position, direction, path)

    heappush(priority_queue, (0, start, 0, []) )

    while priority_queue:
        score, position, direction, path = heappop(priority_queue)
        x: int = position[0]
        y: int = position[1]

        if data[x][y] == 'E':
            return score

        for modify_direction in [0, -1, 1]:
            new_direction = (direction + modify_direction) % 4
            new_x = x + directions[new_direction][0]
            new_y = y + directions[new_direction][1]

            # check whether we reached a wall
            if data[new_x][new_y] != '#' and tuple([new_x, new_y]) not in visited:
                new_score = score + 1 if new_direction == direction else score + 1001
                heappush(priority_queue, (new_score, [new_x, new_y], new_direction, path + [new_direction] ) )
                visited.add( tuple([new_x, new_y]) )

    # if the queue is empty, we did not find a solution
    return np.inf


def find_all_best_paths_BFS(
    data: List[List[str]],
    start: List[int],
    score: int,
) -> List[Tuple[int, List[int]]]:

    visited = {}  # {(x, y): best_score}

    # store the score and the path of the best paths found so far
    best_paths: List[Tuple[int, List[int]]] = []

    priority_queue: List[Tuple[int, List[int], int, int, List[int]]] = []  # (score, position, direction, path)

    heappush(priority_queue, (0, start, 0, []) )

    same_score: bool = True

    while priority_queue and same_score:
        score, position, direction, path = heappop(priority_queue)

        if len(best_paths) > 0 and score > best_paths[0][0]:
            same_score = False
            break

        x: int = position[0]
        y: int = position[1]

        if data[x][y] == 'E':
            # check if this still has the best score
            if len(best_paths) > 0:
                if score > best_paths[0][0]:
                    same_score = False
                    break

            best_paths.append( (score, path) )
            # print(f'Found a good solution (time: {time.time() - t0:.1f}s): {score = }, {path = } continieng search ...')
            # update same_score if there is two entries in best_paths

            continue

        if (x, y) in visited and visited[(x, y)] < score - 1000:
            continue

        visited[(x, y)] = score

        for modify_direction in [0, -1, 1]:
            new_direction = (direction + modify_direction) % 4
            new_x = x + directions[new_direction][0]
            new_y = y + directions[new_direction][1]

            # check whether we reached a wall
            if data[new_x][new_y] != '#':
                new_score = score + 1 if new_direction == direction else score + 1001
                # if this score exceeds the best score, we can stop
                if len(best_paths) > 0 and new_score > best_paths[0][0]:
                    same_score = False
                    break
                heappush(priority_queue, (new_score, [new_x, new_y], new_direction, path + [new_direction] ) )

    # if the queue is empty, we did not find a solution
    return best_paths

# write function that uses the path directions as input and outputs the path as locations
def path_to_locations(
    start: List[int],
    path: List[int],
) -> List[Tuple[int]]:

    locations: List[Tuple[int]]= [ tuple(start) ]
    for direction in path:
        locations.append( tuple([ locations[-1][0] + directions[direction][0], locations[-1][1] + directions[direction][1] ]) )

    return locations


starting_point: List[int] = find_start(data)
# print(f'{starting_point}')

finish: List[int] = find_finish(data)
# print(f'{finish}')


# PART 1

# # recursive DFS solution (does not terminate for full problem)

# straight_initial = find_possible_paths_DFS(
#     data = data,
#     position = starting_point,
#     score = 1,
#     direction = 0,
# )

# left_initial = find_possible_paths_DFS(
#     data = data,
#     position = starting_point,
#     score = 1001,
#     direction = 1,
# )

# right_initial = find_possible_paths_DFS(
#     data = data,
#     position = starting_point,
#     score = 1001,
#     direction = 3,
# )

# # scores: List[Tuple[int, List[int]]] = sorted( [straight_initial, left_initial, right_initial], key=lambda x:x[0])
# scores: List[int] = sorted( [straight_initial, left_initial, right_initial] )

# # print(f'{scores = }')

# # print(f'{scores[0][0] = }')
# # print(f'{len(scores[0][1]) = }')

# print(f'{scores[0] = }')


# iterative BFS solution:

score = find_possible_paths_BFS(
    data = data,
    start = starting_point,
    score = 1,
)

print(f'{score = }')

# # PART 2

best_paths = find_all_best_paths_BFS(
    data = data,
    start = starting_point,
    score = 1,
)

# print(f'{best_paths = }')
# print(f'{len(best_paths) = }')

paths_as_locations: List[List[Tuple[int, int]]] = [path_to_locations(starting_point, path) for score, path in best_paths]

# print(f'{paths_as_locations[0] = }')
# print(f'{paths_as_locations[1] = }')
# print(f'{paths_as_locations[2] = }')

visitied_by_any: List[Tuple[int, int]] = list(set( [location for path in paths_as_locations for location in path] ))

print(f'{len(visitied_by_any) = }')

t1 = time.time()
print(f"Time it took: {t1-t0:.1f}s")
