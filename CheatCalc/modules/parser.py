from enum import IntEnum
from collections import namedtuple
from . import isInt, bin2dec, TType, CusChar, relatPath


class KMode(IntEnum):
    norm = 0
    sf = 1
    alpha = 2

IOPair = namedtuple('IOPair', 'IN OUT')


def parseKeyLayout():
    lines = open(relatPath('../key-layout.txt')).read().splitlines()
    keys = [[[] for j in range(3)] for i in range(int(lines.pop(0)))]
    for l in lines:
        tokens = l.split()
        if len(tokens) == 0 or not isInt(tokens[0]):
            continue
        n = int(tokens.pop(0))
        kmode = KMode.norm
        for t in tokens:
            if t == '%':
                kmode = KMode.sf
            elif t == '@':
                kmode = KMode.alpha
            else:
                ttype = TType.text
                if t.startswith('%'):
                    t = t[1:]
                    if '@' != t != '%':
                        ttype = TType[t]
                elif '@' in t:
                    ttype = TType.func
                # insert token in the right slot
                keys[n][kmode].append((t, ttype))
    return keys


def parseKeyPins():
    lines = open(relatPath('../key-pins.txt')).read().splitlines()
    inPins = [0] * 4
    outPins = [0] * 8
    n = int(lines.pop(0))
    ioCodes = [[] for i in range(int(n))]
    for l in lines:
        tkns = l.split()
        if len(tkns) == 0:
            continue
        elif isInt(tkns[0]):
            ioCodes[int(tkns[0])] = IOPair(int(tkns[1]), int(tkns[2]))
        elif tkns[0] == 'in':
            for i in range(4):
                inPins[i] = int(tkns[i + 1])
        elif tkns[0] == 'out':
            for i in range(8):
                outPins[i] = int(tkns[i + 1])
    return n, inPins, outPins, ioCodes


def parseNotes():
    lines = open(relatPath('../notes.txt'),
                 encoding='utf-8').read().splitlines()
    notes = []
    comment = False
    for l in lines:
        tkns = l.split()
        if len(tkns) > 0:
            if tkns[0].startswith('%title'):
                notes.append([l[len(tkns[0]):].strip(), [], []])
            elif tkns[0].startswith('%tags'):
                notes[-1][1] = tkns[1:]
            elif tkns[0].startswith('%%%'):
                comment = not comment
            elif not comment and not tkns[0].startswith('%%'):
                notes[-1][2] += [l[i:i + 15] for i in range(0, len(l), 15)]
    return notes

# return [( name, [[bool]] )]


def parseCusChars():
    lines = open(relatPath('../custom-chars.txt')).read().splitlines()
    chars = []
    charLineCount = 8
    for l in lines:
        tkns = l.split()
        if len(tkns) > 0:
            first = tkns[0]
            if charLineCount != 8:
                chars[-1][1][charLineCount] = bin2dec(
                    [1 if x == '#' else 0 for x in l[::2]][::-1])
                charLineCount += 1
            if first.startswith('$'):
                chars.append([CusChar[first[1:-1]], [0] * 8])
            elif first == '+':
                charLineCount = 0
            elif first.startswith('+'):
                i = next(x for x in range(len(chars)) if chars[x][
                    0] == CusChar[first[1:]])
                chars[-1][1] = [chars[-1][1][j] | chars[i][1][j]
                                for j in range(8)]
    return chars

# return [( [name, args...], impl )]


def parseMacros():
    lines = open(relatPath('../macros.txt')).read().splitlines()
    macros = []
    for l in lines:
        tkns = l.split()
        if len(tkns) > 0:
            first = tkns[0]
            if first.startswith('%'):
                continue
            idx = first.find('(') + 1
            name = first[:idx - 1]
            params = []
            while True:
                newidx = first.find(',', idx)
                if newidx == -1:
                    params.append((first[idx:len(first) - 1], []))
                    break
                params.append((first[idx:newidx], []))
                idx = newidx + 1
            params = [x for x in params if x[0] != '']
            idx = 0
            string = l[l.find(tkns[1]):]
            while idx < len(string):
                paridx = [x for x in range(len(params))
                          if string[idx:].startswith(params[x][0])
                          and (idx == 0 or not string[idx - 1].isalnum())
                          and (idx + len(params[x][0]) >= len(string)
                               or not string[idx + len(params[x][0])].isalnum())]
                if len(paridx) == 0:
                    idx += 1
                    continue
                paridx = paridx[0]
                params[paridx][1].append(idx)
                parlen = len(params[paridx][0])
                string = string[:idx] + string[idx + parlen:]
            macros.append((name, params, string))
    # generate matrix macros
    for y in range(1, 7):
        for x in range(1, 7):
            name = '@' + str(y) + str(x)
            params = []
            string = ''
            for y1 in range(y):
                string += ',' if y1 > 0 else '{'
                for x1 in range(x):
                    string += ',' if x1 > 0 else '{'
                    params.append(('', [len(string)]))
                string += '}'
            string += '}'
            macros.append((name, params, string))
    return macros
