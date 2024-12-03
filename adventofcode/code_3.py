file1 = open('input_3.txt', 'r')
Lines = file1.readlines()

horizontal = 0
depth = 0

for line in Lines:
    line_arr = line.split(" ")
    if 'forward' in line:
        horizontal += int(line_arr[1])
    elif 'down' in line:
        depth += int(line_arr[1])
    elif 'up' in line:
        depth -= int(line_arr[1])

print(horizontal)
print(depth)

print(horizontal * depth)