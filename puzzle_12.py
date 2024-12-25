#! /usr/bin/python3

import numpy as np
from typing import List, Tuple

import time

infile: str = "./puzzle_12_input.txt"

f = open(infile, "r")

data: List[List[str]] = [ [ char for char in string ] for string in f.read().split('\n') ]


def find_garden_regions(
    data: List[List[str]],
    current_row: int,
    current_column: int,
    field_counter: int,
    this_crop: str,
    area: int = 0,
    perimeter: int = 0
) -> Tuple[List[List[str]], int, int, int]:

    # time.sleep(0.5)
    # print_map(data)

    # check if the current position is a valid field
    if current_row < 0 or current_row >= len(data) or current_column < 0 or current_column >= len(data[0]):
        return data, area, perimeter + 1, field_counter

    # print(f'Checking field {current_row},{current_column} with value {data[current_row][current_column]}')

    if data[current_row][current_column] == f"#{field_counter}":
        return data, area, perimeter, field_counter

    if data[current_row][current_column] != this_crop:
        return data, area, perimeter + 1, field_counter

    # if the current position is a field, mark it as visited
    # print(f'Setting the value of the field to {f"#{field_counter}"}')
    data[current_row][current_column] = f"#{field_counter}"
    area += 1

    # check the 4 directions
    data, area, perimeter, field_counter = find_garden_regions(data, current_row-1, current_column, field_counter, this_crop, area, perimeter)
    data, area, perimeter, field_counter = find_garden_regions(data, current_row+1, current_column, field_counter, this_crop, area, perimeter)
    data, area, perimeter, field_counter = find_garden_regions(data, current_row, current_column-1, field_counter, this_crop, area, perimeter)
    data, area, perimeter, field_counter = find_garden_regions(data, current_row, current_column+1, field_counter, this_crop, area, perimeter)

    return data, area, perimeter, field_counter


# for part 1
def calculate_total_price(regions: List[Tuple[str, int, int, str]]) -> int:

    total_price: int = 0

    for region in regions:
        total_price += region[1] * region[2]

    return total_price


# for part 2
def calculate_total_price_extended(regions_extended: List[Tuple[str, int, int, str, int]]) -> int:

    total_price: int = 0

    for region_extended in regions_extended:
        total_price += region_extended[1] * region_extended[4]

    return total_price


def print_map(
        crops: List[List[str]],
        filename: str = './puzzle_12_output.txt'
        ) -> None:

    try:
        f = open(filename, "r+")
        f.truncate(0)
        f.close()
    except FileNotFoundError:
        pass

    f = open(filename, "w")

    for x in range(len(crops)):
        for y in range(len(crops[0])):
            f.write(crops[x][y])
        f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()


# PART 1

# loop over all entries in the data array

all_garden_regions: List[Tuple[str, int, int, str]] = list()
field_counter:int = 0

# print_map(data)

for i in range(len(data)):

    for j in range(len(data[0])):

        # if this is a field that was not counted before start finding the whole garden region including this:
        if not data[i][j].startswith('#'):
            current_crop: str = data[i][j]
            data, this_area, this_perimeter, field_counter = find_garden_regions(
                data = data,
                current_row = i,
                current_column = j,
                field_counter = field_counter,
                this_crop = current_crop,
            )

            # print(f'{data = }')

            # store data and increase field counter
            all_garden_regions.append( (current_crop, this_area, this_perimeter, f"#{field_counter}" ) )
            field_counter += 1

    #     break
    # break

# print(f'{all_garden_regions = }')

total_price: int = calculate_total_price(all_garden_regions)

print(f'{total_price = }')


# PART 2

fields: np.ndarray = np.array( [ np.array(row) for row in data ] )

# print(f"{fields = }")

all_garden_regions_extended: List[Tuple[str, int, int, str, int]] = list()


# attempt of part 2
for garden_region in all_garden_regions:

    corners: List[List[int]] = [[ 0 for i in range(len(data) + 1)] for j in range(len(data[0]) + 1)]

    current: str = garden_region[3]

    # if not current == "#2":
    #     continue

    this_locations = np.where( fields == current )

    # print(f"Checking field: {current}")

    for i in range(len(this_locations[0])):
        row, col = this_locations[0][i], this_locations[1][i]

        # print(f'Checking this location: {row = }, {col = }')

        # check how many corners this field has!

        # top left:

        # print(f'Checking top left corner:')

        if ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
        and (not row - 1 < 0 and not col - 1 < 0 and fields[row - 1][col - 1] == current)
        ):
            # print(f'Adding corner (case 0): {row}{col}')
            corners[row][col] = 2

        if ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
        and (row - 1 < 0 or col - 1 < 0 or fields[row - 1][col - 1] != current)
        ):
            # print(f'Adding corner (case 1): {row}{col}')
            corners[row][col] = 1

        elif ( (not col - 1 < 0 and fields[row][col - 1] == current)
        and (not row - 1 < 0 and not col - 1 < 0 and fields[row - 1][col - 1] == current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
         ):
            # print(f'Adding corner (case 2): {row}{col}')
            corners[row][col] = 1

        elif ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (not row - 1 < 0 and not col - 1 < 0 and fields[row - 1][col - 1] == current)
        and (not row - 1 < 0 and fields[row - 1][col] == current)
         ):
            # print(f'Adding corner (case 3): {row}{col}')
            corners[row][col] = 1


        # top right:

        # print(f'Checking top right corner:')

        if ( (col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
        and (not row - 1 < 0 and not col + 1 >= len(data[0]) and fields[row - 1][col + 1] == current)
        ):
            # print(f'Adding corner (case 0): {row}{col + 1}')
            corners[row][col + 1] = 2

        if ( (col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
        and (row - 1 < 0 or col + 1 >= len(data[0]) or fields[row - 1][col + 1] != current)
        ):
            # print(f'Adding corner (case 1): {row}{col + 1}')
            corners[row][col + 1] = 1

        elif ( (not col + 1 >= len(data[0]) and fields[row][col + 1] == current)
        and (not row - 1 < 0 and not col + 1 >= len(data[0]) and fields[row - 1][col + 1] == current)
        and (row - 1 < 0 or fields[row - 1][col] != current)
         ):
            # print(f'Adding corner (case 2): {row}{col + 1}')
            corners[row][col + 1] = 1

        elif ((col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (not row - 1 < 0 and not col + 1 >= len(data[0]) and fields[row - 1][col + 1] == current)
        and (not row - 1 < 0 and fields[row - 1][col] == current)
         ):
            # print(f'Adding corner (case 3): {row}{col + 1}')
            corners[row][col + 1] = 1


        # bottom left:

        # print(f'Checking bottom left corner:')

        if ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
        and (not row + 1 >= len(data) and not col - 1 < 0 and fields[row + 1][col - 1] == current)
        ):
            # print(f'Adding corner (case 0): {row}{col + 1}')
            corners[row + 1][col] = 2

        if ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
        and (row + 1 >= len(data) or col - 1 < 0 or fields[row + 1][col - 1] != current)
        ):
            # print(f'Adding corner (case 1): {row + 1}{col}')
            corners[row + 1][col] = 1

        elif ( (not col - 1 < 0 and fields[row][col - 1] == current)
        and (not row + 1 >= len(data) and not col - 1 < 0 and fields[row + 1][col - 1] == current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
         ):
            # print(f'Adding corner (case 2): {row + 1}{col}')
            corners[row + 1][col] = 1

        elif ( (col - 1 < 0 or fields[row][col - 1] != current)
        and (not row + 1 >= len(data) and not col - 1 < 0 and fields[row + 1][col - 1] == current)
        and (not row + 1 >= len(data) and not fields[row + 1][col] == current)
         ):
            # print(f'Adding corner (case 3): {row + 1}{col}')
            corners[row + 1][col] = 1


        # bottom right:

        # print(f'Checking bottom right corner:')

        if ( (col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
        and (not row + 1 >= len(data) and not col + 1 >= len(data[0]) and fields[row + 1][col + 1] == current)
        ):
            # print(f'Adding corner (case 0): {row}{col + 1}')
            corners[row + 1][col + 1] = 2

        if ( (col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
        and (row + 1 >= len(data) or col + 1 >= len(data[0]) or fields[row + 1][col + 1] != current)
        ):
            # print(f'Adding corner (case 1): {row + 1}{col + 1}')
            corners[row + 1][col + 1] = 1

        elif ( (not col + 1 >= len(data[0]) and fields[row][col + 1] == current)
        and (not row + 1 >= len(data) and not col + 1 >= len(data[0]) and fields[row + 1][col + 1] == current)
        and (row + 1 >= len(data) or fields[row + 1][col] != current)
         ):
            # print(f'Adding corner (case 2): {row + 1}{col + 1}')
            corners[row + 1][col + 1] = 1

        elif ( (col + 1 >= len(data[0]) or fields[row][col + 1] != current)
        and (not row + 1 >= len(data) and not col + 1 >= len(data[0]) and fields[row + 1][col + 1] == current)
        and (not row + 1 >= len(data) and fields[row + 1][col] == current)
         ):
            # print(f'Adding corner (case 3): {row + 1}{col + 1}')
            corners[row + 1][col + 1] = 1

    # print(f"{corners = }")

    straight_fence: int = sum ( sum(row) for row in corners)

    all_garden_regions_extended.append(
        (
            garden_region[0],
            garden_region[1],
            garden_region[2],
            garden_region[3],
            straight_fence
        )
    )

    # break

    # print(f"{straight_fence = }")

    # break

# print(f'{all_garden_regions_extended = }')

total_price_reduced: int = calculate_total_price_extended(all_garden_regions_extended)

print(f'{total_price_reduced = }')
