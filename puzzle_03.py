#! /usr/bin/python3

import re
import numpy as np

from typing import List

infile: str = "./puzzle_3_input.txt"

f = open(infile, "r")
data = f.read().replace('\n', '')


# PART 1

def clean_data(data: str) -> List[str]:
    pattern: str = r"mul[(][0-9]*,[0-9]*[)]"
    return re.findall(pattern, data)

def calculate_line(data: str) -> int:
    pattern: str = r"[0-9]+"
    numbers = re.findall(pattern, data)
    return int(numbers[0]) * int(numbers[1])

uncorrupted_line = clean_data(data)
total_sum: int = sum((calculate_line(string) for string in uncorrupted_line))

print(f"{total_sum = }")


# PART 2

def split_data(data: str) -> List[str]:
    pattern: str = r"do[(][)]|don't[(][)]|mul[(][0-9]*,[0-9]*[)]"  # just finds either match (single return)
    # pattern: str = r"(do[(][)])|(don't[(][)])|(mul[(][0-9]*,[0-9]*[)])"  %  # splits in regex groubs (3 returns)
    return re.findall(pattern, data)

total_sum_better: int = 0

split_line = split_data(data)

# print(f"{split_line = }")

activated: bool = True

for entry in split_line:

    # print(f"{entry = }")

    if entry.startswith("do()"):
        activated = True

    elif entry.startswith("don't()"):
        activated = False

    elif activated:
        total_sum_better += calculate_line(entry)

print(f"{total_sum_better = }")
