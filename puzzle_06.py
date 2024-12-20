#! /usr/bin/python3

import sys
sys.setrecursionlimit(18000)
import numpy as np

from collections import Counter

from typing import List, Dict, Tuple

import copy

infile: str = "./puzzle_6_input.txt"

f = open(infile, "r")

# data: List[str] = f.readlines()
# data: List[List[str]] = [string.split() for string in f.read().split('\n')]

data: List[str] = f.read().split('\n')

data_new: List[List[str]] = list()

for string in data:
    data_new.append( [char for char in string] )

data_original: List[List[str]] = copy.deepcopy( data_new )

# data = [string.split() for string in data]

# print(f'{data_new = }')
# print(f'{len(data_new) = }')
# print(f'{len(data_new[0]) = }')


# PART 1

directions: List[str] = ['^','>','v','<']

def take_step(data: List[List[str]], i: int, j: int, direction_count: int) -> List[List[str]]:

    # mark position as visited (X)
    data[i][j] = 'X'

    # print(f'Trying to step from {i},{j} in direction {directions[direction_count]}')

    i_step: int = -1
    j_step: int = -1

    if direction_count == 0:
        i_step = i - 1
        j_step = j
    elif direction_count == 1:
        i_step = i
        j_step = j + 1
    elif direction_count == 2:
        i_step = i + 1
        j_step = j
    elif direction_count == 3:
        i_step = i
        j_step = j - 1

    # check boundary conditions of the matrix
    if i_step < 0 or i_step >= len(data) or j_step < 0 or j_step >= len(data[0]):
        return data

    if data[i_step][j_step] not in ['.', 'X']:
        # switch direction and take step again
        direction_count = ( direction_count + 1 ) % 4
        return take_step(data, i, j, direction_count)
    else:
        # continue stepping in the same direction
        return take_step(data, i_step, j_step, direction_count)

    return data

# find starting point and start iteration

start_i: int = -1
start_j: int = -1

for i in range(len(data_new)):
    for j in range(len(data_new[0])):
        if data_new[i][j] == directions[0]:
            start_i = i
            start_j = j

# start stepping through the grid recursively
print(f'Found start at ({start_i},{start_j})!')
data_new = take_step(data_new, start_i, start_j, 0)
# break


# print(f'{data_new = }')
# print(f'{Counter(data_new[10]) = }')

number_of_distinct_positions: int = 0

for row in data_new:
    row_counter = Counter(row)
    if 'X' in row_counter.keys():
        # print(f'{row_counter = }')
        number_of_distinct_positions += row_counter['X']

# print(f'{data_new = }')
print(f'{number_of_distinct_positions = }')


# PART 2

def take_step_and_check_loop(data: List[List[str]], i: int, j: int, direction_count: int, visited_count: int) -> Tuple[List[List[str]], int]:

    # print(f'{visited_count = }')

    # check if this position was already visited
    if data[i][j] == 'X':
        visited_count += 1
    else:
        visited_count = 0

    if visited_count > 4 * len(data):
        return data, visited_count

    # mark position as visited (X)
    data[i][j] = 'X'

    # print(f'Trying to step from {i},{j} in direction {directions[direction_count]}')

    i_step: int = -1
    j_step: int = -1

    if direction_count == 0:
        i_step = i - 1
        j_step = j
    elif direction_count == 1:
        i_step = i
        j_step = j + 1
    elif direction_count == 2:
        i_step = i + 1
        j_step = j
    elif direction_count == 3:
        i_step = i
        j_step = j - 1

    # check boundary conditions of the matrix
    if i_step < 0 or i_step >= len(data) or j_step < 0 or j_step >= len(data[0]):
        # print("Walked outside of the grid..")
        return data, visited_count

    if data[i_step][j_step] not in ['.', 'X']:
        # switch direction and take step again
        direction_count = ( direction_count + 1 ) % 4
        return take_step_and_check_loop(data, i, j, direction_count, visited_count)

    # continue stepping in the same direction
    return take_step_and_check_loop(data, i_step, j_step, direction_count, visited_count)


# make new grid that can be modified
data_modified: List[List[str]] = list()

visited_count: int = 0
working_loops: int = 0

for i in range(len(data_original)):
    for j in range(len(data_original[0])):

        if data_original[i][j] == '.':

            # make copy of the original and work with this
            data_modified = copy.deepcopy( data_original )

            # add obstacle here
            data_modified[i][j] = '#'

            # print(data_modified)

            # start stepping through the grid recursively
            data_modified, visited_count = take_step_and_check_loop( data_modified, start_i, start_j, 0, visited_count )

            # print(f'{visited_count = }')

            if visited_count > 4 * len(data_modified):
                working_loops += 1

    #     break
    # break

print(f'{working_loops = }')
