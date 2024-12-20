#! /usr/bin/python3

import numpy as np
import pandas as pd

import copy

import collections

infile: str = "./puzzle_2_input.txt"

data = pd.read_csv(infile, header=None).fillna(0).values

# print(f"{data = }")
# print(f"{np.shape(data) = }")


# print(f"{(data[:10]) = }")

def is_safe(levels: str) -> bool:
    levels = [int(level) for level in levels.split()]
    # print(f"{levels = }")

    differences = np.array(levels[1:]) - np.array(levels[:-1])
    # print(f"{differences = }")

    monotonic = all(differences > 0) or all(differences < 0)
    smaller_3 = all(abs(differences) <= 3)

    return monotonic and smaller_3

# print(f"{is_safe(data[0][0]) = }")

safe_list = [ is_safe(entry[0]) for entry in data ]

# print(f"{(safe_list[:10]) = }")

total_sum_safe = sum(safe_list)

print(f"{total_sum_safe = }")


# brute force solution
def is_safe_dampened_brute_force(levels: str) -> bool:
    levels = [int(level) for level in levels.split()]
    differences = np.array(levels[1:]) - np.array(levels[:-1])

    monotonic = all(differences > 0) or all(differences < 0)
    smaller_3 = all(abs(differences) <= 3)

    standard_case = monotonic and smaller_3

    if standard_case:
        return True
    else:
        for i in range(len(levels)):
            reduced_levels = copy.deepcopy(levels)
            reduced_levels.pop(i)

            differences = np.array(reduced_levels[1:]) - np.array(reduced_levels[:-1])

            monotonic = all(differences > 0) or all(differences < 0)
            smaller_3 = all(abs(differences) <= 3)

            if monotonic and smaller_3:
                return True

        return False

safe_list_dampened = [ is_safe_dampened_brute_force(entry[0]) for entry in data ]

total_sum_safe_dampened = sum(safe_list_dampened)

print(f"Brute force solution: {total_sum_safe_dampened = }")


# ugly af solution, but it works
def is_safe_dampened(levels: str) -> bool:
    levels = [int(level) for level in levels.split()]

    # print(f"{levels = }")

    differences = np.array(levels[1:]) - np.array(levels[:-1])

    monotonic = all(differences > 0) or all(differences < 0)
    smaller_3 = all(abs(differences) <= 3)

    standard_case = monotonic and smaller_3
    always_bad_case = monotonic and not smaller_3

    if standard_case:
        return True
    elif always_bad_case:
        if sum(abs(differences) > 3) == 1 and np.where(abs(differences) > 3)[0][0] == 0 or np.where(abs(differences) > 3)[0][0] == len(differences) - 1:
            # print(f"{levels = }")
            # print(f"{differences = }")
            return True
        return False
    else:
        # print(f"{levels = }")

        occurances = collections.Counter(levels).most_common(1)[0][1]
        # print(f"{occurances = }")
        if occurances > 2:
            # print(f"{levels = }")
            # print(f"{occurances = }")
            return False

        # damping case 1: one value doubled (removing it, solves the problem)
        double_value = all(differences >= 0) and sum(differences == 0) == 1 or all(differences <= 0) and sum(differences == 0) == 1

        if double_value and smaller_3:
            # print(f"has double value and monotonic: {levels = }")
            return True
        elif double_value and not smaller_3:
            return False

        # if more than 2 differences are positive and negative, fail
        if sum(differences > 0) > 1 and sum(differences < 0) > 1:
            return False

        # print(f"{levels = }")
        # print(f"{differences = }")

        # damping case 2: one value decreasing/increasing
        monotonic_up = sum(differences > 0) > 1 and sum(differences < 0) == 1
        monotonic_down = sum(differences < 0) > 1 and sum(differences > 0) == 1

        # find out which can be made possible by removing one value
        if monotonic_up:
            index = np.where(differences < 0)
        elif monotonic_down:
            index = np.where(differences > 0)
        else:
            return False

        damping_2 = False

        # print(f"{levels = }")
        # print(f"{differences = }")

        # remove the value that is not monotonic

        index = index[0][0]
        # print(f"{index = }")

        reduced_levels_1 = copy.deepcopy(levels)
        reduced_levels_1.pop(index)

        # print(f"{reduced_levels_1 = }")
        reduced_differences_1 = np.array(reduced_levels_1[1:]) - np.array(reduced_levels_1[:-1])
        reduced_monotonic_1 = all(reduced_differences_1 > 0) or all(reduced_differences_1 < 0)

        reduced_smaller_3_1 = all(abs(reduced_differences_1) <= 3)

        damping_2 = reduced_monotonic_1 and reduced_smaller_3_1

        # if that did not work, try index + 1
        if not damping_2:
            reduced_levels_2 = copy.deepcopy(levels)
            reduced_levels_2.pop(index+1)

            # print(f"{reduced_levels_2 = }")
            reduced_differences_2 = np.array(reduced_levels_2[1:]) - np.array(reduced_levels_2[:-1])
            reduced_monotonic_2 = all(reduced_differences_2 > 0) or all(reduced_differences_2 < 0)

            reduced_smaller_3_2 = all(abs(reduced_differences_2) <= 3)

            damping_2 = reduced_monotonic_2 and reduced_smaller_3_2

        # print(f"{damping_2 = }")

        return damping_2

safe_list_dampened = [ is_safe_dampened(entry[0]) for entry in data ]

total_sum_safe_dampened = sum(safe_list_dampened)

print(f"Ugly solution: {total_sum_safe_dampened = }")
