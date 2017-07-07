from enum import IntEnum
from .. import isInt
from . import CursorView, TType
import modules

class ListMode(IntEnum):
    fixNum = 0
    scrollNum = 1


class List(CursorView):

    def __init__(self, parent, actList, lmode=ListMode.scrollNum):
        super().__init__(parent)
        self._lmode = lmode  # ListMode.fixNum
        self._oldTime = 0
        self._cursor = [1, 0]
        self._actList = []
        self.updateActList(actList)
        # print(self._text)

    def updateActList(self, actList):
        # actlist: from [(text, action)] to [(text, action, scrolltext)]
        print('updating ActList')
        self._actList = [[x, y, False] if len(
            x) <= 16 - 3 else [x + '    ', y, True] for x, y in actList]
        self.clearRows()
        self.addRows([str(x + 1) + ' ' + self._actList[x][0]
                      for x in range(len(actList))])

    def loop(self):
        super().loop()
        c = self._cursor[1]
        if self._actList[c][2] and modules.timeNow - self._oldTime > 0.6:
            self._oldTime = modules.timeNow
            scrl = 2
            self._actList[c][0] = self._actList[c][
                0][scrl:] + self._actList[c][0][:scrl]
            self.changeRow(self._actList[c][0], start=2, rIdx=c)
        if self._lmode == ListMode.fixNum:
            if self._rows > 0:
                self.changeRow('1', end=1, rIdx=self._screenPos[1])
                if self._rows > 1:
                    self.changeRow('2', end=1, rIdx=self._screenPos[1] + 1)

    def procCmd(self, t1, t2):
        if t2 == TType.text and isInt(t1) and t1 != '0' and int(t1) - 1 < self._rows:
            if self._lmode == ListMode.fixNum:
                if t1 == '1' or t1 == '2':
                    self._actList[self._screenPos[1] + int(t1) - 1][1]()
            else:
                self._actList[int(t1) - 1][1]()
            self.closeMe()
        if t2 == TType.enter:
            self._actList[self._cursor[1]][1]()
            self.closeMe()
        elif t2 != TType.left and t2 != TType.right:
            super().procCmd(t1, t2)
