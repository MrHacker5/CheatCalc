from modules import parser
macros = parser.parseMacros()

def expandMacros(inp):
    idx = len(inp) - 3
    while idx >= 0:
        macroidx = [x for x in range(len(macros))
                    if inp[idx:].startswith(macros[x][0])
                    and (idx == 0 or not inp[idx - 1].isalnum())
                    and (idx + len(macros[x][0]) >= len(inp)
                         or inp[idx + len(macros[x][0])] == '(')]
        if len(macroidx) == 0:
            idx -= 1
            continue
        macroidx = macroidx[0]
        params = []
        paramidx = idx + len(macros[macroidx][0]) + 1
        laststartidx = paramidx
        layer = 1
        while layer > 0 and paramidx < len(inp):
            char = inp[paramidx]
            if char in '([{':
                layer += 1
            else:
                if layer == 1 and char in ',)':
                    if paramidx != laststartidx:
                        params.append(inp[laststartidx:paramidx])
                    laststartidx = paramidx + 1
                if char in ')]}':
                    layer -= 1
            paramidx += 1
        if layer != 0 or len(params) != len(macros[macroidx][1]):
            idx -= 2
            continue  # the input is invalid, leave the macro not replaced
        inp = inp[:idx] + macros[macroidx][2] + \
            (inp[paramidx:] if paramidx < len(inp) else '')
        paramidx = idx + len(macros[macroidx][2])
        while paramidx >= 0:
            idxarr = [x for x in range(len(macros[macroidx][1]))
                      if paramidx - idx in macros[macroidx][1][x][1]]
            if len(idxarr) != 0:
                inp = inp[:paramidx] + params[idxarr[0]] + inp[paramidx:]
            paramidx -= 1
        idx = len(inp) - 3  # restart for recursive macros
    return inp


inp = input()

inp = expandMacros(inp)
# macro are in prefix notation, so parse from end to start


print(inp)
