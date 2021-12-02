file1 = open('input_2.txt', 'r')
Lines = file1.readlines()

count = 0
prev = None
for counter in range(0, len(Lines)):
    if counter+2 < len(Lines):
        number_1 = int(Lines[counter].strip())
        number_2 = int(Lines[counter+1].strip())
        number_3 = int(Lines[counter+2].strip())
        total = number_1 + number_2 + number_3
        if prev and total > prev:
            count += 1
        prev = total

print(count)