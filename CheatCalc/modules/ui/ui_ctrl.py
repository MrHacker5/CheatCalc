from . import TType, graphics


class UI(object):

    def __init__(self, parent):
        self._drawArea = [True] * 32  # all screen
        self.childs = []
        self._parent = parent
        self.enabled = True
        self._canClose = True
        self.deleteOnClose = True

    def loop(self):
        for c in self.childs:
            if c.enabled:
                c.loop()

    # only if there are no child active, process the token (unless the
    # behaviour is overridden)
    def procToken(self, token):
        listEnab = [x for x in self.childs if x.enabled]
        if listEnab:
            listEnab[-1].procToken(token)
        else:
            self.procCmd(token[0], token[1])

    def procCmd(self, t1, t2):
        pass

    def draw(self):
        for i in range(32):
            if self._drawArea[i]:
                graphics.screen[i] = self.drawChar(i)
        for c in self.childs:
            if c.enabled:
                c.draw()

    def drawChar(self, i):
        return ' '

    def closeMe(self):
        print('closing')
        print(type(self))
        if self._canClose:
            if self.deleteOnClose:
                self._parent.childs.remove(self)
            else:
                self.enabled = False

    def clearArea(self):
        for i in self._drawArea:
            graphics.screen[i] = ' '
