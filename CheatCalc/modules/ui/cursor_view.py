from . import TType, CusChar, View, graphics

_cusCharList = [x for x in CusChar]


class CursorView(View):

    def __init__(self, parent, rows=None):
        super().__init__(parent, rows)
        self._cursor = [0, 0]

    def loop(self):
        super().loop()
        c0, c1 = self._cursor
        s0, s1 = self._screenPos
        if c0 - s0 < 3:
            self._screenPos[0] = max(c0 - 3, 0)
        elif c0 - s0 > 13:
            # +1 to fix InputField
            self._screenPos[0] = min(c0 - 13, self._cols - 14 + 1)
        if c1 - s1 < 0:
            self._screenPos[1] = c1
        elif c1 - s1 > 1:
            self._screenPos[1] = min(c1 - 1, self._rows - 2)
        s0, s1 = self._screenPos  # update
        # print(type(self))
        # print(self._cursor)
        # print(self._screenPos)
        if len([x for x in self.childs if x.enabled]) == 0:  # don't steal focus
            graphics.cursor = (c0 - s0, c1 - s1)
            graphics.cursorEnabled = True

    def procCmd(self, t1, t2):
        c0, c1 = self._cursor
        if t2 == TType.up and c1 > 0:
            self._cursor[1] -= 1
        elif t2 == TType.down and c1 < self._rows - 1:
            self._cursor[1] += 1
        elif t2 == TType.left and c0 > 0:
            self._cursor[0] -= 1
        elif t2 == TType.right and c0 < self._cols - 0:
            self._cursor[0] += 1
        else:
            super().procCmd(t1, t2)

    def drawChar(self, i):
        if i != 31:
            return super().drawChar(i)
        else:  # draw appropriate arrow char with bin math
            c = 0
            if self._cursor[1] > 0:
                c += 1
            if self._cursor[1] < self._rows - 1:
                c += 2
            if self._cursor[0] > 0:
                c += 4
            if self._cursor[0] < self._cols - 1:
                c += 8
            return _cusCharList[c]
