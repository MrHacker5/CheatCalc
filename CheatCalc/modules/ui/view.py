from . import UI, TType


class View(UI):

    def __init__(self, parent, rows=None):
        super().__init__(parent)
        self._drawArea[15] = False
        self._screenPos = [0, 0]
        self._text = []
        self._rows = 0
        self._cols = 0
        if rows != None:
            self.addRows(rows)

    def procCmd(self, t1, t2):
        if t2 == TType.bs or t2 == TType.esc:
            self.closeMe()

    def drawChar(self, i):
        # allow last column to be on screen column 15 because of the sf/alpha
        # char
        x = self._screenPos[0] + i % 16
        y = self._screenPos[1] + i // 16
        if 0 <= y < self._rows and 0 <= x < len(self._text[y]):
            return self._text[y][x]
        else:
            return ' '

    def changeRow(self, s='', start=0, end=-1, rIdx=-1):
        if rIdx == -1:
            rIdx = self._rows - 1
        if end == -1:
            end = len(self._text[rIdx])
        self.changeRows(
            [(self._text[rIdx][:start] + s + self._text[rIdx][end:], rIdx)])

    def addRows(self, rows):
        self.changeRows(zip(rows, range(self._rows, self._rows + len(rows))))

    def clearRows(self):
        self.changeRows([(-1, x) for x in range(self._rows)])

    def changeRows(self, rows):
        #print('changingRows')
        #print(type(self))
        adding = [(l, i) for l, i in rows if l != -1]
        if adding:
            maxLen = max([i for l, i in adding]) + 1
            if maxLen > self._rows - 1:
                self._text += [''] * (maxLen - self._rows)
            for l, i in adding:
                self._text[i] = l
        removing = [i for l, i in rows if l == -1]
        if removing:
            removing.sort(reverse=True)
            for i in removing:
                del self._text[i]
        self._rows = len(self._text)
        if self._rows > 0:
            self._cols = max([len(x) for x in self._text])
