file1 = open('input_1.txt', 'r')
Lines = file1.readlines()

count = 0

prev = None
for line in Lines:
    number = int(line.strip())
    if prev and number > prev:
        count += 1
    prev = number

print(count)
