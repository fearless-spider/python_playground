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
