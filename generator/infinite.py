import sys
import cProfile


def infinite_squence():
    num = 0
    while True:
        yield num
        num += 1

#for i in infinite_squence():
#    print(i, end=" ")

gen = infinite_squence()
print(next(gen))

nums_squared_lc = [num**2 for num in range(5)]
nums_squared_gc = (num**2 for num in range(5))

print(nums_squared_lc)
print(nums_squared_gc)

nums_squared_lc = [num*2 for num in range(100000)]
print(sys.getsizeof(nums_squared_lc))

nums_squared_gc = (num*2 for num in range(100000))
print(sys.getsizeof(nums_squared_gc))

cProfile.run('sum((num*2 for num in range(100000)))')
