file1 = open('input_8.txt', 'r')
Lines = file1.readlines()

bingo_numbers = Lines[0].split(",")
bingo_tables = []
bingo_tables_all = []
found_bingo = []
found_bingo_number = []
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

for number in bingo_numbers:
    for i in range(0, len(bingo_tables_all)):
        if i not in found_bingo:
            bingo = False
            for j in range(0, 5):
                total = 0
                for k in range(0, 5):
                    if int(number) == bingo_tables_all[i][j][k]:
                        bingo_tables_all[i][j][k] = 0
                    total += bingo_tables_all[i][j][k]
                if total == 0:
                    found_bingo.append(i)
                    found_bingo_number.append(int(number))
                    bingo = True
                    break
                if bingo:
                    continue
                total = 0
                for k in range(0, 5):
                    total += bingo_tables_all[i][k][j]
                if total == 0:
                    found_bingo.append(i)
                    found_bingo_number.append(int(number))
                    break

print(found_bingo)
print(bingo_tables_all[found_bingo[-1]])
summary = 0
for i in range(0,5):
    for j in range(0,5):
        summary += bingo_tables_all[found_bingo[-1]][i][j]
print(summary)
print(found_bingo_number[-1])
print(summary*found_bingo_number[-1])