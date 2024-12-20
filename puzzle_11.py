#! /usr/bin/python3

import time
t0 = time.time()

import numpy as np
from typing import List, Dict

infile: str = "./puzzle_11_input.txt"

f = open(infile, "r")

data: List[int] = [int(string) for string in f.readline().split(' ')]
# data: np.ndarray = np.array([int(string) for string in f.readline().split(' ')])

print(f'{data = }')
# print(f'{len(data) = }')


def blink(data: List[int]) -> List[int]:
# def blink(data: np.ndarray) -> np.ndarray:

    new_data: List[int] = list()
    # new_data_length: int = len(data) + sum([len(str(entry)) % 2 == 0 for entry in data])
    # new_data = np.zeros(new_data_length, dtype=int)

    # i: int = 0
    for number in data:
        # print(f'{number = }')

        string = str(number)

        if number == 0:
            new_data.append(1)
            # new_data[i] = 1
            # i += 1

        elif len(string) % 2 == 0:
            # split number in half
            first_half: int = int(string[:len(string) // 2])
            second_half: int = int(string[len(string) // 2:])

            new_data.append(first_half)
            new_data.append(second_half)
            # new_data[i] = first_half
            # new_data[i + 1] = second_half
            # i += 2

        else:
            # multiply by 2024 and write
            new_data.append(number * 2024)
            # new_data[i] = number * 2024
            # i += 1

    return new_data


def blink_dict(data_dict: Dict[int, int]) -> Dict[int, int]:

    new_data: Dict[int, int] = dict()

    for key, item in data_dict.items():

        string = str(key)

        if key == 0:
            if 1 in new_data.keys():
                new_data[1] += item
            else:
                new_data[1] = item

        elif len(string) % 2 == 0:
            # split number in half
            first_half: int = int(string[:len(string) // 2])
            second_half: int = int(string[len(string) // 2:])

            if first_half in new_data.keys():
                new_data[first_half] += item
            else:
                new_data[first_half] = item

            if second_half in new_data.keys():
                new_data[second_half] += item
            else:
                new_data[second_half] = item

        else:
            new_key: int = key * 2024

            if new_key in new_data.keys():
                new_data[new_key] += item
            else:
                new_data[new_key] = item

    return new_data


# Try it using a list (works for first 25, but breaks later)

# # test length calculation
# split_bool = [len(str(entry)) % 2 == 0 for entry in data]
# print(f'{split_bool = }')

# new_data = len(data) + sum(split_bool)
# print(f'{new_data = }')


# # PART 1
# for i in range(25):

# # # PART 2
# # for i in range(75):

#     if i % 10 == 0:
#         print(f'{i = }')
#         tstep = time.time()
#         print(f"Time it took: {tstep-t0:.1f}s")
#     # print(f'{i = }')

#     data = blink(data)
#     # print(f'{data = }')

#     # break

# # print(f'{data = }')
# print(f'{len(data) = }')


# Same thing using a dictionary

data_dict: Dict[int, int] = dict()  # {key is the number, value is the number of times it appears}

for number in data:
    if number in data_dict:
        data_dict[number] += 1
    else:
        data_dict[number] = 1

print(f'{data_dict = }')


# # PART 1
# for i in range(25):

# PART 2
for i in range(75):

    if i % 10 == 0:
        print(f'{i = }')
        tstep = time.time()
        print(f"Time it took: {tstep-t0:.1f}s")
    # print(f'{i = }')

    data_dict = blink_dict(data_dict)
    # print(f'{data_dict = }')

    # break

# print(f'{data = }')
print(f'{sum(data_dict.values()) = }')



t1 = time.time()
print(f"Time it took: {t1-t0:.1f}s")
