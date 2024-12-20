#! /usr/bin/python3

import numpy as np

from typing import List, Dict, Tuple

from collections import Counter

infile: str = "./puzzle_10_input.txt"

f = open(infile, "r")

data: np.ndarray = np.array([[int(char) for char in string] for string in f.read().split('\n')])


# print(f'{data = }')
# print(f'{data.shape = }')

# print(f'{len(data) = }')
# print(f'{len(data[0]) = }')

# print(f'{type(data) = }')
# print(f'{type(data[0]) = }')


def find_unique_paths(data: np.ndarray, position: np.ndarray, reachable_summits: List[Tuple[int]], current_value:int = -1) -> List[Tuple[int]]:

    # print(f"Checking position {position} (value: {data[position[0], position[1]]}), with previous height of {current_value}.")

    # check whether this follows the correct scope
    if position[0] < 0 or position[0] >= data.shape[0] or position[1] < 0 or position[1] >= data.shape[1] or data[position[0], position[1]] - current_value != 1:
        return reachable_summits

    # stopping criterion
    if data[position[0], position[1]] == 9:
        # add this to the list of reachable ones
        # print(f'Found reachable summit at: {tuple((position[0], position[1])) = }')
        # print(f'It has the entry: {data[position[0], position[1]] = }')
        reachable_summits.append( tuple(position.tolist()) )
        return reachable_summits

    # if we are not there yet, find further paths from this point
    reachable_summits = find_unique_paths(data, position + [1,0], reachable_summits, current_value + 1)
    reachable_summits = find_unique_paths(data, position + [-1,0], reachable_summits, current_value + 1)
    reachable_summits = find_unique_paths(data, position + [0,1], reachable_summits, current_value + 1)
    reachable_summits = find_unique_paths(data, position + [0,-1], reachable_summits, current_value + 1)

    return reachable_summits


# PART 1

trailheads: np.ndarray = np.array(np.where(data == 0)).T
# print(f'{trailheads = }')
# print(f'{trailheads[0] = }')
# print(f'{trailheads[0]+[1,0] = }')

trailhead_counts: List[int] = list()
trailhead_rating: List[int] = list()

for trailhead in trailheads:
    # print(f'{trailhead = }')

    # print(f'{data[trailhead[0], trailhead[1]] = }')

    these_reachable_summits: List[Tuple[int]] = list()
    these_reachable_summits = find_unique_paths(data, trailhead, these_reachable_summits)

    # print(f'{(these_reachable_summits) = }')
    # print(f'{set(these_reachable_summits) = }')

    # PART 1

    trailhead_counts.append( len(set(these_reachable_summits)) )
    # print(f'{trailhead_counts = }')

    # PART 2

    trailhead_rating.append( len(these_reachable_summits) )
    # print(f'{trailhead_rating = }')

    # break

# print(f'{trailhead_counts = }')
print(f'{sum(trailhead_counts) = }')

# print(f'{trailhead_rating = }')
print(f'{sum(trailhead_rating) = }')
