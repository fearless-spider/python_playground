file1 = open('input_6.txt', 'r')
Lines = file1.readlines()

power_consumption = 0  # gamma_rate * epsilon_rate
gamma_rate = 0
epsilon_rate = 0

common_one = [0] * (len(Lines[0])-1)
for line in Lines:
    for i in range(0, len(common_one)):
        if line[i] == "1":
            common_one[i] += 1

bit_criteria = []
bit_criteria2 = []
for bit in common_one:
    if bit >= len(Lines)/2:
        bit_criteria.append(1)
        bit_criteria2.append(0)
    else:
        bit_criteria.append(0)
        bit_criteria2.append(1)

counter = 0
oxygen_lines = Lines
scrubber_lines = Lines
for bit in bit_criteria:
    temp = []
    for line in oxygen_lines:
        if str(bit) == line[counter]:
            temp.append(line.strip())
    if counter < len(bit_criteria)-1:
        common_one[counter + 1] = 0
        for line in temp:
            if line[counter+1] == "1":
                common_one[counter+1] += 1

        if common_one[counter+1] >= round(len(temp) / 2):
            bit_criteria[counter+1] = 1
        else:
            bit_criteria[counter+1] = 0

    if len(temp) == 0:
        break

    oxygen_lines = temp
    counter += 1

counter = 0
for bit in bit_criteria2:
    temp = []
    for line in scrubber_lines:
        if str(bit) == line[counter]:
            temp.append(line.strip())

    if counter < len(bit_criteria2)-1:
        common_one[counter + 1] = 0
        for line in temp:
            if line[counter+1] == "0":
                common_one[counter+1] += 1

        if common_one[counter+1] <= round(len(temp) / 2):
            bit_criteria2[counter+1] = 0
        else:
            bit_criteria2[counter+1] = 1
    if len(temp) == 0:
        break

    scrubber_lines = temp
    counter += 1


counter = len(oxygen_lines[0])-1
for bit in oxygen_lines[0]:
    epsilon_rate += int(bit) * (2 ** counter)
    counter -= 1

counter = len(scrubber_lines[0])-1
for bit in scrubber_lines[0]:
    gamma_rate += int(bit) * (2 ** counter)
    counter -= 1

print(epsilon_rate)
print(gamma_rate)
print(epsilon_rate*gamma_rate)