#! /usr/bin/python3

import re
import numpy as np

from typing import List

infile: str = "./puzzle_4_input.txt"

f = open(infile, "r")
data: List[str] = f.readlines()


# PART 1

# write recursive function to find word XMAS
def find_word_recursive(data: List[str], i: int, j: int, letter_count: int, direction: List[int]) -> bool:

    # check boundary conditions of the matrix
    if i < 0 or i >= len(data) or j < 0 or j >= len(data[0]) - 1 or letter_count >= len(search_word):
        return False

    if data[i][j] != search_word[letter_count]:
        return False

    if letter_count == len(search_word) - 1:
        return True

    return find_word_recursive(data, i + direction[0], j + direction[1], letter_count + 1, direction)

search_word: str = "XMAS"

# go through all entries and if I hit an X, start DFS search for the word XMAS
rows: int = len(data)
cols: int = len(data[0])

found_words: int = 0

for i in range(rows):
    for j in range(cols):
        # DFS search for the word XMAS in all directions
        if find_word_recursive(data, i, j, 0, [1, 0]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [0, 1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [1, 1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [-1, 1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [1, -1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [-1, -1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [0, -1]):
            found_words += 1
        if find_word_recursive(data, i, j, 0, [-1, 0]):
            found_words += 1

print(f"{found_words = }")

# PART 2

# search for MAS appearing in an X pattern

found_words_2: int = 0

for i in range(1, rows - 1):
    for j in range(1, cols - 1):
        if data[i][j] == "A":
            # check for MAS in both diagonal directions
            diag_one: bool = data[i - 1][j - 1] == "M" and data[i + 1][j + 1] == "S" or data[i - 1][j - 1] == "S" and data[i + 1][j + 1] == "M"
            diag_two: bool = data[i - 1][j + 1] == "M" and data[i + 1][j - 1] == "S" or data[i - 1][j + 1] == "S" and data[i + 1][j - 1] == "M"

            if diag_one and diag_two:
                found_words_2 += 1

print(f"{found_words_2 = }")
