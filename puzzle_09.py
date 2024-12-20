#! /usr/bin/python3

import time

t0 = time.time()

from typing import List

from collections import OrderedDict

import numpy as np

infile: str = "./puzzle_9_input.txt"

f = open(infile, "r")

data: np.ndarray = np.array([char for char in f.readlines()[0]])

# print(f'{data = }')
# print(f'{len(data) = }')
# print(f'{len(data[0]) = }')


def expand_input_data(data: np.ndarray) -> OrderedDict:

    expanded_data: OrderedDict = OrderedDict()

    position_counter: int = 0
    data_id_counter: int = 0

    for i, entry in enumerate(data):
        # free spaces
        if i % 2 == 0:
            # print(f'Writing current data id starting at location {i} with length {entry}')
            for j in range(int(entry)):
                expanded_data[position_counter] = str(data_id_counter)
                position_counter += 1
            data_id_counter += 1
        else:
            # print(f'Writing empty spaces starting at location {i} with length {entry}')
            for j in range(int(entry)):
                expanded_data[position_counter] = '.'  # not sure if this is a good value..
                position_counter += 1

    return expanded_data


def compactify_data(data: OrderedDict) -> OrderedDict:

    # start two pointers at beginning and back of data, move the towareds each other, where beginning pointer is always the next empty space and the back pointer is always the next data id

    # write the data id from the back pointer to the beginning pointer (clearing the space at the back pointer)

    empty_pointer: int = 0
    data_pointer: int = len(data) - 1

    while empty_pointer < data_pointer:
        # find empty spaces
        if data[empty_pointer] != '.':
            empty_pointer += 1

        # find data ids
        if data[data_pointer] == '.':
            data_pointer -= 1

        # swap the two values
        # only swap if empty pointer is pointing to an empty space and data pointer is pointing to a data id
        if data[empty_pointer] == '.' and data[data_pointer] != '.':
            data[empty_pointer] = data[data_pointer]
            data[data_pointer] = '.'

    return data


def calculate_checksum(data: OrderedDict) -> int:
    # loop through the dict and calculate id times position for each entry and sum the result
    checksum: int = 0

    for i, entry in data.items():
        if entry != '.':
            # print(f'{i = }')
            # print(f'{entry = }')
            checksum += int(entry) * i

    return checksum


def compactify_data_smarter(data: OrderedDict) -> OrderedDict:

    # start two pointers at beginning and back of data, move the towareds each other, where beginning pointer is always the next empty space and the back pointer is always the next data id

    # find out how long the current empty space is and how long the current data id is

    # only if the empty space is longer (or same length) as the data id, move the data to the empty space and clear the data space

    # if the data id is longer than the empty space, try the next empty space..

    # only try every data id once

    empty_pointer: int = 0
    data_pointer: int = len(data) - 1

    data_id_length: int = 0
    empty_space_length: int = 0

    while data_pointer - data_id_length > 0:

        # find data ids
        if data[data_pointer] == '.':
            data_pointer -= 1
            continue

        # if a data id was found, find length of this data id
        if data[data_pointer] != '.' and data_id_length == 0:
            # print(f'Found data id at {data_pointer}')
            # count from here until the next empty space
            data_id_length = 1

            # print(f'Checking data at {data_pointer - data_id_length}')

            while data_pointer - data_id_length >= 0 and data[data_pointer - data_id_length] == data[data_pointer]:
                data_id_length += 1
            # print(f'Found data id length: {data_id_length}')


        # data was found and length established:
        if data[data_pointer] != '.' and data_id_length != 0:

            # loop over all potential empty spaces and try to move them

            empty_pointer = 0
            empty_space_length = 0

            while empty_pointer <= data_pointer - data_id_length:

                # print(f"{data_pointer = }")
                # print(f"{data_id_length = }")
                # print(f"{empty_pointer = }")

                # find empty spaces
                if data[empty_pointer] != '.':
                    empty_pointer += 1

                # if an empty spot was found, find length of this empty spot
                if data[empty_pointer] == '.' and empty_space_length == 0:
                    # print(f'Found empty space at {empty_pointer}')
                    # count from here until the next data id
                    empty_space_length = 1
                    while data[empty_pointer + empty_space_length] == '.':
                        empty_space_length += 1
                    # print(f'Found empty space length: {empty_space_length}')


                # write the data id to the empty space if the empty space is longer or same length as the data id
                if empty_space_length and data_id_length and empty_space_length >= data_id_length:

                    for i in range(data_id_length):
                        # print(f'Moving data from {data_pointer - i} to empty space {empty_pointer}')
                        data[empty_pointer] = data[data_pointer - i]
                        data[data_pointer - i] = '.'
                        empty_pointer += 1

                    data_pointer -= data_id_length
                    data_id_length = 0

                    empty_pointer = 0
                    empty_space_length = 0

                    # current_data_print: str = "".join(data.values())
                    # print(f'{current_data_print = }')

                    break

                else:
                    # empty_space_length and data_id_length and empty_space_length < data_id_length:

                    # print(f'Empty space is too short, moving to next empty space')
                    empty_pointer += empty_space_length
                    empty_space_length = 0

                # if empty_pointer >= data_pointer - data_id_length:
                #     # print(f'No more empty spaces available, resetting empty pointer to beginning of data')
                #     # reset empty pointer to the beginning of the data
                #     empty_pointer = 0
                #     # move down to next data id
                #     data_pointer -= data_id_length

            else:
                data_pointer -= data_id_length
                data_id_length = 0

    return data


# Expand data first

expanded_data: OrderedDict = expand_input_data(data)

# print(f'{expanded_data.keys() = }')
# print(f'{expanded_data.values() = }')

# print(len(expanded_data))

expanded_data_combined: str = "".join(expanded_data.values())

# print(f'{expanded_data_combined = }')



# # PART 1

# compacted_data: OrderedDict = compactify_data(expanded_data)

# # print(f'{compacted_data.keys() = }')
# # print(f'{compacted_data.values() = }')

# # print(len(compacted_data))

# compacted_data_combined: str = "".join(compacted_data.values())

# # print(f'{compacted_data_combined = }')


# checksum: int = calculate_checksum(compacted_data)

# print(f'{checksum = }')


# PART 2

compacted_data_smarter: OrderedDict = compactify_data_smarter(expanded_data)

# print(f'{compacted_data_smarter.keys() = }')
# print(f'{compacted_data_smarter.values() = }')

# print(len(compacted_data_smarter))

compacted_data_smarter_combined: str = "".join(compacted_data_smarter.values())

# print(f'{compacted_data_smarter_combined = }')


checksum_smarter: int = calculate_checksum(compacted_data_smarter)

print(f'{checksum_smarter = }')

t1 = time.time()

print(f"Time it took: {t1-t0:.1f}s")
