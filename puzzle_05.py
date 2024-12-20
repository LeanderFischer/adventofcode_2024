#! /usr/bin/python3

import re
import numpy as np

from typing import List, Dict

infile: str = "./puzzle_5_input.txt"

f = open(infile, "r")
data = f.read()

# print(f"{data = }")

orderings = data.split("\n\n")[0].split("\n")
pages = data.split("\n\n")[1].split("\n")

# print(f"{orderings = }")
# print(f"{type(orderings[0]) = }")

# print(f"{pages = }")

# turn orderings into a dict, with key as lower page and list of numbers as value
orderings_dict: Dict[int, List[int]] = {}
for entry in orderings:
    entries: List[str] = entry.split("|")

    key: int = int(entries[0])
    value: int = int(entries[1])

    if key in orderings_dict:
        orderings_dict[key].append(value)
    else:
        orderings_dict[key] = [value]

total_middle_pages_correct: int  = 0
total_middle_pages_corrected: int  = 0

def check_ordering(print_list: List[int]) -> bool:

    for pos, val in enumerate(print_list):
        if not val in orderings_dict.keys():
            continue
        else:
            for pos_smaller in range(pos-1, -1, -1):
                if print_list[pos_smaller] not in orderings_dict[val]:
                    continue
                else:
                    return False
    return True

def correct_ordering(print_list: List[int]) -> List[int]:

    while not check_ordering(print_list):

        for pos, val in enumerate(print_list):
            if not val in orderings_dict.keys():
                continue
            else:
                for pos_smaller in range(pos-1, -1, -1):
                    if print_list[pos_smaller] in orderings_dict[val]:
                        print_list.insert(pos+1, print_list.pop(pos_smaller))
    return print_list


for update in pages:
    update_list = [ int(x) for x in update.split(',') ]

    correctly_ordered: bool = check_ordering(update_list)


    # PART 1

    if len(update_list) % 2 == 1 and correctly_ordered:
        total_middle_pages_correct += update_list[int( (len(update_list) - 1) / 2)]


    # PART 2

    if not correctly_ordered:
        update_list = correct_ordering(update_list)
        total_middle_pages_corrected += update_list[int( (len(update_list) - 1) / 2)]

    # break

print(f"{total_middle_pages_correct = }")
print(f"{total_middle_pages_corrected = }")