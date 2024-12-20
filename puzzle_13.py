#! /usr/bin/python3

import time

t0 = time.time()

import numpy as np

from sympy import linsolve
from sympy.abc import x, y

from typing import List, Tuple

import re

infile: str = "./puzzle_13_input.txt"

f = open(infile, "r")

data: List[str] = f.readlines()


def extract_machine_information(data: List[str]) -> Tuple[List[int], List[int], List[int]]:

    button_a: List[int] = [int(x) for x in re.findall(r'\d+', data[0])]
    button_b: List[int] = [int(x) for x in re.findall(r'\d+', data[1])]
    price_position: List[int] = [int(x) for x in re.findall(r'\d+', data[2])]

    # print(f'{button_a = }')
    # print(f'{button_b = }')
    # print(f'{price_position = }')

    return button_a, button_b, price_position


def check_reachability(button_a: List[int], button_b: List[int], price_position: List[int]) -> Tuple[bool, List[Tuple[int, int]]]:

    a: np.ndarray = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])
    b: np.ndarray = np.array(price_position)

    solutions = list( linsolve(
        [
            button_a[0] * x + button_b[0] * y - price_position[0],
            button_a[1] * x + button_b[1] * y - price_position[1]
        ],
        [x, y],
    ) )

    # print(f'{(solutions) = }')
    # print(f'{type(solution) = }')
    # print(f'{[x.is_integer for x in solution] = }')
    # print('')

    # only integer solutions are valid
    return all([x.is_integer and y.is_integer for x, y in solutions]), solutions


def find_all_possible_ways(
        button_a: List[int],
        button_b: List[int],
        price_position: List[int],
        checked_positions: List[List[int]],
        all_ways: List[Tuple[int, int]],
        steps_a: int = 0,
        steps_b: int = 0,
    ) -> Tuple[List[Tuple[int, int]], List[List[int]]]:

    # print(f'{steps_a = }')
    # print(f'{steps_b = }')

    # check if we already tested these steps
    if [steps_a, steps_b] in checked_positions:
        return all_ways, checked_positions
    else:
        checked_positions.append([steps_a, steps_b])

    if [steps_a * button_a[0] + steps_b *button_b[0], steps_a * button_a[1] + steps_b *button_b[1]] == price_position:
        # print(f"Reached price position {price_position}!")
        # add this way to the list of all ways
        all_ways.append( tuple((steps_a, steps_b)) )
        return all_ways, checked_positions

    if steps_a * button_a[0] + steps_b *button_b[0] > price_position[0] or steps_a * button_a[1] + steps_b *button_b[1] > price_position[1]:
        return all_ways, checked_positions

    # check if steps_a + 1 is valid and if so, try it:
    if not steps_a + 1 * button_a[0] + steps_b *button_b[0] > price_position[0] or not steps_a + 1 * button_a[1] + steps_b * button_b[1] > price_position[1]:
        all_ways, checked_positions = find_all_possible_ways(button_a, button_b, price_position, checked_positions, all_ways, steps_a + 1, steps_b)

    # check if steps_b + 1 is valid and if so, try it:
    if not steps_a * button_a[0] + steps_b + 1 *button_b[0] > price_position[0] or not  steps_a * button_a[1] + steps_b + 1 * button_b[1] > price_position[1]:
        all_ways, checked_positions = find_all_possible_ways(button_a, button_b, price_position, checked_positions, all_ways, steps_a, steps_b + 1)

    return all_ways, checked_positions

def find_cheapest_way(all_ways: List[Tuple[int, int]]) -> int:
    # price for step a is 3 and for step b is 1
    return min([3 * x + y for x, y in all_ways])


# print(f'{data = }')
# print(f'{data[0] = }')

# print(f'{type(data) = }')
# print(f'{type(data[0]) = }')

# print(f'{len(data) = }')
# print(f'{len(data[0]) = }')


# # PART 1

# total_price: int = 0

# for i in range( int((len(data) + 1) / 4) ):
#     # get next 3 lines
#     this_machine_raw_input: List[str] = data[i*4:i*4+3]
#     # print(f"{this_machine_raw_input = }")

#     # extract machine information
#     this_machine_info: Tuple[List[int], List[int], List[int]] = extract_machine_information(this_machine_raw_input)
#     # print(f"{this_machine_info = }")

#     # check reachability
#     reachable, solutions = check_reachability(this_machine_info[0], this_machine_info[1], this_machine_info[2])
#     # print(f"{reachable = }")


#     if reachable:
#         # print(f"Machine {i+1} can be reached with {solutions} steps.")

#         checked_positions: List[List[int]] = list()
#         all_ways: List[Tuple[int, int]] = list()

#         all_ways_possible, checked_positions = find_all_possible_ways(
#             this_machine_info[0],
#             this_machine_info[1],
#             this_machine_info[2],
#             checked_positions,
#             all_ways,
#             )
#         # print(f"{(all_ways_possible) = }")
#         # print(f"{set(all_ways_possible) = }")

#         cheapest_way: int = find_cheapest_way(all_ways_possible)
#         # print(f"{cheapest_way = }")

#         total_price += cheapest_way

#     # if i == 20:
#     #     break

# print(f"{total_price = }")


# PART 2 (better way to solve the problem!!!)

total_price: int = 0

for i in range( int((len(data) + 1) / 4) ):
    # get next 3 lines
    this_machine_raw_input: List[str] = data[i*4:i*4+3]
    # print(f"{this_machine_raw_input = }")

    # extract machine information
    this_machine_info: Tuple[List[int], List[int], List[int]] = extract_machine_information(this_machine_raw_input)
    # print(f"{this_machine_info = }")

    # add 10000000000000 to the price position
    this_machine_info = (this_machine_info[0], this_machine_info[1], [x + 10000000000000 for x in this_machine_info[2]])
    # print(f"{this_machine_info = }")

    # check reachability
    reachable, solutions = check_reachability(this_machine_info[0], this_machine_info[1], this_machine_info[2])
    # print(f"{reachable = }")


    if reachable:
        # print(f"Machine {i+1} is reachable!")
        # print(f"Machine {i+1} can be reached with {solutions} steps.")

        # just use the found solutions as the way to go
        all_ways_possible = solutions

        # print(f"{(all_ways_possible) = }")
        # print(f"{set(all_ways_possible) = }")

        cheapest_way: int = find_cheapest_way(all_ways_possible)
        # print(f"{cheapest_way = }")

        total_price += cheapest_way

    # if i == 20:
    #     break

    # break

print(f"{total_price = }")


t1 = time.time()

print(f"Time it took: {t1-t0:.1f}s")
