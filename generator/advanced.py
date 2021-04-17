def is_polindrome(num):
    # Skip single-digit inputs
    if num // 10 == 0:
        return False

    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False

def infinite_polindromes():
    num = 0
    while True:
        if is_polindrome(num):
            i = (yield num)
            if i is not None:
                num = i
        num += 1

pal_gen = infinite_polindromes()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    pal_gen.send(10 ** (digits))
