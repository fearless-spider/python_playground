def new_strip(data, c=' '):
    buf = ""
    result = []

    for x in data:
        if x == c:
            result.append(buf)
            buf = ""
        else:
            buf += x

    result.append(buf)
    return result

print(new_strip("ala ma kota"))

def new_strip_gen(data, c=' '):
    buf = ""
    result = []
    d = (x for x in data)

    try:
        while True:
            a = next(d)
            if a == c:
                result.append(buf)
                buf = ""
            else:
                buf += a
    except StopIteration:
        pass

    result.append(buf)
    return result

print(new_strip_gen("ala ma kota"))
