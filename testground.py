from itertools import accumulate
from collections import deque

scale = [0, 2, 2, 1, 2, 2, 2, 1]
indices = [sum(scale[:i]) for i in range(len(scale) + 1)][:-1]
# print(list(accumulate([0, 2, 2, 1, 2, 2, 2, 1]))[:-1])
# print(scale[:-1])

d = deque(scale)


a = [0, 1, 1, 1, 2, 3, 4, 5]

d = deque(a)

# Rotate 2 positions to the right
d.rotate(2)

# Convert back to list if needed
rotated_list = [d]
print(rotated_list)
