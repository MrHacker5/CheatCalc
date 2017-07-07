from . import TType, CusChar, CursorView
print('ok') 
from .. import parser

_cusCharList = [x for x in CusChar]

macros = parser.parseMacros()

class InputField(CursorView):
    shiftCaps = 0
    hist = ['']

    def __init__(self, parent, action):
        super().__init__(parent, IF.hist + [''])
        self._cursor = [0, self._rows - 1]
        self._drawArea[:14] = [False] * 14
        self._action = action  # called when enter is pressed

    def procCmd(self, t1, t2):
        c = self._cursor[0]
        if t2 == TType.bs:
            if c != 0:
                self.changeRow('', c - 1, c)
                self._cursor[0] -= 1
        elif t2 == TType.shift or t2 == TType.caps:
            if IF.shiftCaps == 0:
                if t2 == TType.shift:
                    IF.shiftCaps = 1
                else:
                    IF.shiftCaps = 2
            else:
                IF.shiftCaps = 0
        elif t2 == TType.caps:
            IF.shiftCaps = 2
        elif t2 in [TType.text, TType.func, TType.space]:
            if self._cursor[1] != self._rows - 1:
                #print('field overridden')
                self.changeRow(self._text[self._cursor[1]])
                self._cursor[1] = self._rows - 1
            if t2 == TType.space:
                t1 = ' '
            elif t2 == TType.func:  # todo implement ergument selection with tab
                i = t1.index('@')
                t1 = t1.replace('@', '')
                self._cursor[0] += i
            if len(t1) == 1:
                t1 = t1.upper() if IF.shiftCaps > 0 else t1.lower()
            if t2 != TType.func:
                self._cursor[0] += len(t1)
            self.changeRow(t1, c, c)
        elif t2 == TType.enter:
            if self._text[-1] != '':  # save input to hist
                IF.hist.append(self._text[-1])
            self._text[-1] = expandMacros(self._text[-1])
            self._action(self._text[-1])
            self.closeMe()
        else:
            if t2 == TType.up:
                # if out of bounds it will be fixed in CursorView's loop
                self._screenPos[1] -= 1
                self._cursor[0] = 0
            if t2 == TType.down and self._cursor[1] != self._rows - 1:
                self._screenPos[1] += 1
                self._cursor[0] = 0
            if not (t2 == TType.right and self._cursor[0] >= len(self._text[self._cursor[1]])):
                super().procCmd(t1, t2)
        if t2 != TType.shift and IF.shiftCaps == 1:
            IF.shiftCaps = 0

    

    def drawChar(self, i):
        if i != 14:
            return super().drawChar(i)
        else:
            return _cusCharList[18 if IF.shiftCaps == 1 else 19 if IF.shiftCaps == 2 else 0]


IF = InputField

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
