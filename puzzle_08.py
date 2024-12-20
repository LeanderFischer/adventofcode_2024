#! /usr/bin/python3

from typing import List
from collections import Counter

import math

import numpy as np

infile: str = "./puzzle_8_input.txt"

f = open(infile, "r")

data: List[List[str]] = [ [ char for char in string ] for string in f.read().split('\n') ]

# print(f'{data = }')
# print(f'{len(data) = }')
# print(f'{len(data[0]) = }')


all_data: List[str] = [ char for sublist in data for char in sublist ]

number_of_chars = Counter(all_data)
# print(f'{number_of_chars = }')

double_chars = [key for key, value in number_of_chars.items() if value > 1 and key != '.']
# print(f'{double_chars = }')


# PART 1

antinodes: List[List[int]] = list()

for char in double_chars:
    # print(f'{char = }')

    positions = np.array(np.where(np.array(data) == char)).T
    # print(f'{positions = }')

    for i, pos_i in enumerate(positions):
        for j in range(i+1, len(positions)):
            pos_j = positions[j]

            # print(f"{pos_i = }")
            # print(f"{pos_j = }")

            distance = (pos_j - pos_i)
            # print(f'{distance = }')

            antinode = (pos_i - distance)
            # print(f'{antinode = }')

            if not (antinode < 0).any() and not (antinode > len(data) - 1).any() and not antinode.tolist() in antinodes:
                antinodes.append(antinode.tolist())

            antinode = (pos_j + distance)
            # print(f'{antinode = }')

            if not (antinode < 0).any() and not (antinode > len(data) - 1).any() and not antinode.tolist() in antinodes:
                antinodes.append(antinode.tolist())

    #         break
    #     break
    # break

# print(f'{antinodes = }')
print(f'{len(antinodes) = }')


# PART 2

antinodes_updated: List[List[int]] = list()

for char in double_chars:
    # print(f'{char = }')

    positions = np.array(np.where(np.array(data) == char)).T
    # print(f'{positions = }')

    for i, pos_i in enumerate(positions):
        for j in range(i+1, len(positions)):
            pos_j = positions[j]

            # print(f"{pos_i = }")
            # print(f"{pos_j = }")

            distance = (pos_j - pos_i)
            # print(f'{distance = }')

            gcd: int = math.gcd(distance[0], distance[1])
            # print(f'{gcd = }')

            distance = np.array([int(distance[0] / gcd), int(distance[1] / gcd)])
            # print(f'{distance = }')

            # step away from pos_i
            antinode = pos_j - distance
            while (antinode >= 0).all() and (antinode < len(data)).all():
                # print(f'{antinode = }')
                if not antinode.tolist() in antinodes_updated:
                    antinodes_updated.append(antinode.tolist())
                antinode -= distance

            # step towareds pos_j
            antinode = pos_i + distance
            while (antinode >= 0).all() and (antinode < len(data)).all():
                # print(f'{antinode = }')
                if not antinode.tolist() in antinodes_updated:
                    antinodes_updated.append(antinode.tolist())
                antinode += distance

            # break
    #     break
    # break

# print(f'{sorted(antinodes_updated) = }')
print(f'{len(antinodes_updated) = }')
