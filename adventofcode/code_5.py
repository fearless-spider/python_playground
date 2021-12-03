file1 = open('input_5.txt', 'r')
Lines = file1.readlines()

power_consumption = 0  # gamma_rate * epsilon_rate
gamma_rate = 0
epsilon_rate = 0

common_one = [0] * (len(Lines[0])-1)
for line in Lines:
    for i in range(0, len(common_one)):
        if line[i] == "1":
            common_one[i] += 1

counter = len(common_one)-1
for bit in common_one:
    if bit > len(Lines)/2:
        gamma_rate += 2 ** counter
    else:
        epsilon_rate += 2 ** counter
    counter -= 1

print(gamma_rate)
print(epsilon_rate)
power_consumption = gamma_rate * epsilon_rate
print(power_consumption)