def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def dec2bin(d):
    b = []
    while len(b) < 4:
        b.append(d % 2 == 0)
        d //= 2
    return b


def bin2dec(b):
    d = 0
    l = len(b)
    for i in range(l):
        d += b[i] * 2**i
    return d
