numbers = [1,2,3,4,5]
squered = []

for number in numbers:
    squered.append(number**2)

print(squered)

def square(number):
    return number ** 2

squered = map(square, numbers)

print(squered)
print(list(squered))

squered = map(lambda num: num ** 2, numbers)

print(squered)
print(list(squered))

import math

def is_positive(num):
    return num >= 0

def sanitized_sqrt(numbers):
    cleaned_iter = map(math.sqrt, filter(is_positive, numbers))
    return list(cleaned_iter)

print(sanitized_sqrt([25, 9, 81, -16, 0]))


import functools
import operator
import os
import os.path

files = os.listdir(os.path.expanduser("~"))
total = functools.reduce(operator.add, map(os.path.getsize, files))
