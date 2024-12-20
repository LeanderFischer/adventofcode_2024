#! /usr/bin/python3

import numpy as np

infile: str = "./puzzle_1_input.txt"

data = np.loadtxt(infile).T

# print(f"{data = }")
# print(f"{np.shape(data) = }")

# print(f"{(data[0][:10]) = }")
# print(f"{(data[1][:10]) = }")

# print(f"{min(data[0]) = }")
# print(f"{min(data[1]) = }")

# print(f"{max(data[0]) = }")
# print(f"{max(data[1]) = }")

list_1_sorted = sorted(data[0])
list_2_sorted = sorted(data[1])

# print(f"{(list_1_sorted[:10]) = }")
# print(f"{(list_2_sorted[:10]) = }")

list_diff = np.array(list_2_sorted) - np.array(list_1_sorted)

# print(f"{(list_diff[:10]) = }")
# print(f"{(list_diff[-10:]) = }")

total_diff: int = int(sum(abs(list_diff)))

print(f"{(total_diff) = }")

from collections import Counter

list_1_counter = Counter(list_1_sorted)
list_2_counter = Counter(list_2_sorted)

# print(f"{(list_1_counter) = }")
# print(f"{(list_2_counter) = }")

# print(f"{(list_2_counter[list_1_sorted[0]]) = }")

similarity_values = [ entry * list_2_counter[entry] for entry in list_1_sorted ]

total_similarity: int = int(sum(similarity_values))

print(f"{(total_similarity) = }")
