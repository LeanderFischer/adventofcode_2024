#! /usr/bin/python3

from typing import List, Tuple, Dict

import os

import time

import copy

import re

import collections

infile: str = "./puzzle_14_input.txt"

f = open(infile, "r")

data: List[str] = f.readlines()

# print(f'{data = }')
# print(f'{data[0] = }')


def extract_robot_information(data: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    position: Tuple[int, int] = tuple((int(re.findall(r'-\d+|\d+', data)[0]), int(re.findall(r'-\d+|\d+', data)[1])))
    velocity: Tuple[int, int] = tuple((int(re.findall(r'-\d+|\d+', data)[2]), int(re.findall(r'-\d+|\d+', data)[3])))

    # print(f'{button_a = }')
    # print(f'{button_b = }')
    # print(f'{price_position = }')

    return position, velocity


def take_steps(
    position: Tuple[int, int],
    velocity: Tuple[int, int],
    steps: int,
    space_x: int,
    space_y: int
    ) -> Tuple[int, int]:

    # print(f"{(position[0] + velocity[0] * steps)}")
    # print(f"{(position[0] + velocity[0] * steps) % space_x}")

    new_position: Tuple[int, int] = tuple(
        (
        (position[0] + velocity[0] * steps) % space_x,
        (position[1] + velocity[1] * steps) % space_y
        )
    )

    return new_position

def print_positions(
    positions: Dict[Tuple[int, int], int],
    seconds: int,
    filename: str = './puzzle_14_output.txt'
) -> None:

    try:
        f = open(filename, "r+")
        f.truncate(0)
        f.close()
    except FileNotFoundError:
        pass


    f = open(filename, "w")

    f.write(str(seconds))
    f.write('\n')
    f.write('\n')

    for x in range(space_x):
        for y in range(space_y):
            if (x, y) in positions:
                f.write(str(positions[(x, y)]))
            else:
                f.write(' ')

        f.write('\n')

    f.close()


def check_symmetry(positions: Dict[Tuple[int, int], int]) -> bool:

    for key, value in positions.items():
        # mirror position along the vertical
        x_mirror = space_x - 1 - key[0]

        if (x_mirror, key[1]) not in positions:
            return False
        if value != positions[(x_mirror, key[1])]:
            return False
    return True


# # PART 1

# # # example space
# # space_x: int = 11
# # space_y: int = 7

# # real space
# space_x: int = 101
# space_y: int = 103

# new_positions: List[Tuple[int, int]] = []

# for line in data:
#     # print(f'{line = }')
#     # print(f'{type(line) = }')

#     position, velocity = extract_robot_information(line)

#     # print(f'{position = }')
#     # print(f'{velocity = }')

#     new_positions.append(take_steps(position, velocity, 100, space_x, space_y))

#     # print(f'{new_positions = }')

#     # break

# # print(f'{sorted(new_positions) = }')
# counter = collections.Counter(new_positions)
# # print(f'{(counter) = }')
# # print(f'{type(counter) = }')

# upper_left: int = 0
# upper_right: int = 0
# lower_left: int = 0
# lower_right: int = 0

# for key, value in counter.items():
#     # print(f'{key = }, {value = }')

#     if key[0] < (space_x - 1)/2 and key[1] < (space_y - 1)/2:
#         upper_left += value
#     elif key[0] > (space_x - 1)/2 and key[1] < (space_y - 1)/2:
#         upper_right += value
#     elif key[0] < (space_x - 1)/2 and key[1] > (space_y - 1)/2:
#         lower_left += value
#     elif key[0] > (space_x - 1)/2 and key[1] > (space_y - 1)/2:
#         lower_right += value

# # print(f'{upper_left = }, {upper_right = }, {lower_left = }, {lower_right = }')

# # multiply them together
# safety_factor: int = 1

# for value in [upper_left, upper_right, lower_left, lower_right]:
#     safety_factor *= value

# print(f'{safety_factor = }')


# PART 2

# real space
space_x: int = 101
space_y: int = 103


# find out how the one tree looks that I found
# tree_seconds: int = 819613
tree_seconds: int = 8179

tree_position: List[Tuple[int, int]] = []

for line in data:

    position, velocity = extract_robot_information(line)

    tree_position.append(take_steps(position, velocity, tree_seconds, space_x, space_y))

tree_counter = collections.Counter(tree_position)
print_positions(tree_counter, tree_seconds)


# time.sleep(1)

# for seconds in range(200, 1000):
# for seconds in range(100000):
for seconds in range(100000):

    break

    # if not seconds == 8114:
    #     continue

    # first kind of symmetry
    # seconds = 42 + 103 * seconds

    # second kind of symmetry (this is the one that will from the tree)
    # seconds = 99 + 101 * seconds

    new_positions: List[Tuple[int, int]] = []

    for line in data:
        # print(f'{line = }')
        # print(f'{type(line) = }')

        position, velocity = extract_robot_information(line)

        # print(f'{position = }')
        # print(f'{velocity = }')

        new_positions.append(take_steps(position, velocity, seconds, space_x, space_y))

    counter = collections.Counter(new_positions)

    if counter == tree_counter:
        print(f'{seconds = }')
        print_positions(counter, seconds)
        break

    # this did not work unfortunately
    # print(f"{check_symmetry(counter) = }")

    # if check_symmetry(counter):
    #     print(f'{seconds = }')
    #     print_positions(counter, f'./puzzle_14_output_{seconds}.txt')

    # print(f'{min(counter.keys()) = }')
    # print(f'{max(counter.keys()) = }')
    print_positions(counter, seconds)

    # time.sleep(1.5)
    # time.sleep(0.7)
    # time.sleep(0.4)

    # if seconds == 0:
    #     break

    # if seconds == 42:
    #     positions_42 = copy.deepcopy(new_positions)
    #     # break

    # if seconds == 99:
    #     positions_99 = copy.deepcopy(new_positions)
    #     # break

    # if seconds == 145:
    #     positions_145 = copy.deepcopy(new_positions)
    #     # break

    # if seconds == 200:
    #     positions_200 = copy.deepcopy(new_positions)
    #     # break

    # if seconds == 248:
    #     break

    # if seconds == 301:
    #     break

    # break

# print(f'{positions_42 == positions_145}')
# print(f'{positions_99 == positions_200}')
