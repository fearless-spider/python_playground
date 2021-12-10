file1 = open('input_7.txt', 'r')
Lines = file1.readlines()

bingo_numbers = Lines[0].split(",")
bingo_tables = []
bingo_win = 0
bingo_row_number = 0
for line in Lines[2:]:
    new_row = []
    if line == '\n':
        continue
    row = line.split(" ")
    for element in row:
        if element == '\n' or element == '':
            continue
        new_row.append(element.strip())
    bingo_tables.append(new_row)

bingo_row_result = [0] * len(bingo_tables)
bingo = False
for number in bingo_numbers:
    counter = 0
    for row in bingo_tables:
        try:
            index = row.index(number)
            bingo_row_result[counter] += 1
            row[row.index(number)] = 0
            if bingo_row_result[counter] == 5:
                bingo = True
                bingo_row_number = counter
                bingo_win = int(number)
                print('Bingo %s' % number)
                break
        except:
            pass
        for c in range(0, 5):
            bingo_test = 0
            for r in range(0, len(bingo_tables)):
                if r % 5 == 0:
                    bingo_test = 0
                bingo_test += int(bingo_tables[r][c])
            if bingo_test == 0:
                bingo = True
                bingo_row_number = counter
                bingo_win = int(number)
                print('Bingo %s' % number)
                break
        counter += 1
    if bingo:
        break

bingo_row_number = bingo_row_number - (bingo_row_number % 5)
total = 0
for row in bingo_tables[bingo_row_number:bingo_row_number+5]:
    for x in row:
        total += int(x)

print(bingo_tables)
print(total*bingo_win)
