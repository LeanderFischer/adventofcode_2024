#! /usr/bin/python3

from typing import List

infile: str = "./puzzle_7_input.txt"

f = open(infile, "r")

data: List[List[str]] = [ string.split(' ') for string in f.read().split('\n') ]

# print(f'{data = }')
# print(f'{len(data) = }')
# print(f'{len(data[0]) = }')


def check_correctness_recursive(result: int, current: int, inputs: List[str],) -> bool:

    # part 1

    if len(inputs) == 1:
        if result == current + int(inputs[0]):
            return True
        elif result == current * int(inputs[0]):
            return result == current * int(inputs[0])
        else:
            return False

    return check_correctness_recursive(result, current + int(inputs[0]), inputs[1:]) or check_correctness_recursive(result, current * int(inputs[0]), inputs[1:])

#     # part 2

#     if len(inputs) == 1:
#         if result == current + int(inputs[0]):
#             return True
#         elif result == current * int(inputs[0]):
#             return result == current * int(inputs[0])
#         else:
#             return result == int(str(current) + inputs[0]
# )
#     return check_correctness_recursive(result, current + int(inputs[0]), inputs[1:]) or check_correctness_recursive(result, current * int(inputs[0]), inputs[1:]) or check_correctness_recursive(result, int(str(current) + inputs[0]), inputs[1:])

total_sum: int = 0

# loop over input and check whether it is correct
for line in data:
    # print(f'{line = }')

    result = int(line[0].split(':')[0])

    # print(f'{result = }')

    inputs = line[2:]
    if check_correctness_recursive(result, int(line[1]), inputs):
        # print(f'{check_correctness_recursive(result, int(line[1]), inputs) = }')
        total_sum += result

    # break

print(f'{total_sum = }')
