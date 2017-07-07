import modules.ui
from . import TType, CursorView, InputField
from .. import Process


class Math(CursorView):

    def __init__(self, parent):
        super().__init__(parent)
        self._proc = Process('wolfram', self._outCb)
        self.openInp()
        self._canClose = False
        self._reqMoveCur = 0

    def loop(self):
        if self._reqMoveCur != 0:
            self._screenPos[1] = self._cursor[1] = self._reqMoveCur
            self._cursor[0] = 0
            self._reqMoveCur = 0
        super().loop()

    def _outCb(self, s):  # ASYNCRONOUS!!!!!!
        # self.rmTrailing()
        s = s.splitlines()
        if s[0].startswith('In['):
            s[0] += self._text[self._rows - 1]
            self.rmTrailing()
            #self._reqMoveCur = 1

        for i in range(len(s)):
            if s[i].startswith('Out['):
                modules.ui.ansNum = int(s[i][4:s[i].index(']')])
                self._reqMoveCur = self._rows + i
        rows = [x for x in s if x != '']  # filter out newlines
        #rows +=['']
        # print(rows)
        self.addRows(rows)
        # self.addRows([''])
        # print(self._text)

    def _inCb(self, s):
        # self.rmTrailing()
        self._screenPos[1] -= 1
        self.addRows([s])
        #self._cursor[1] = self._rows-1
        self._proc.sendInput(s + '\n')
        # self.openInp()  # reopen

    def rmTrailing(self):
        self.changeRows([(-1, self._rows - 1)])  # remove trailing empty row

    def openInp(self):
        self.childs.append(InputField(self, self._inCb))

    def procCmd(self, t1, t2):
        if t2 in [TType.text, TType.func, TType.bottom] or (t2 == TType.down and self._rows - 1 - self._cursor[1] == 0):
            self._screenPos[1] += 1
            self.openInp()
            self.childs[-1].procToken((t1, t2))  # do not lose the token
        else:
            super().procCmd(t1, t2)

    def procClose(self):
        self._proc.close()
