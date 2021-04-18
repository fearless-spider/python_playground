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
