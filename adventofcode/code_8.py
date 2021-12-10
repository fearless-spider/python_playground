file1 = open('input_8.txt', 'r')
Lines = file1.readlines()

bingo_numbers = Lines[0].split(",")
bingo_tables = []
bingo_win = 0
bingo_row_number = 0
bingo_tables_all = []
for line in Lines[2:]:
    new_row = []
    if line == '\n':
        bingo_tables_all.append(bingo_tables)
        bingo_tables = []
        continue
    row = line.split(" ")
    for element in row:
        if element == '\n' or element == '':
            continue
        new_row.append(int(element.strip()))
    bingo_tables.append(new_row)

