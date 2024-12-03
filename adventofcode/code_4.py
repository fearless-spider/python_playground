file1 = open('input_4.txt', 'r')
Lines = file1.readlines()

horizontal = 0
depth = 0
aim = 0

for line in Lines:
    line_arr = line.split(" ")
    if 'forward' in line:
        horizontal += int(line_arr[1])
        depth += int(line_arr[1]) * aim
    elif 'down' in line:
        aim += int(line_arr[1])
    elif 'up' in line:
        aim -= int(line_arr[1])

print(horizontal)
print(depth)

print(horizontal * depth)