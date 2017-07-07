from . import TType, UI, CusChar, View, List, MessageView, MVType, ListMode, Math, Notes, CursorView, InputField
from .. import relatPath
import modules


class Root(UI):

    def __init__(self):
        super().__init__(None)
        self.sf = False
        self.alpha = False
        self._drawArea = [False] * 32
        self._drawArea[15] = True
        self.childs += [Math(self), Notes(self),
                        List(self, [('Mathematica', lambda: self.enableOnly(Math)),
                                    ('Notes', lambda: self.enableOnly(Notes))])]
        self.childs[-1]._canClose = False
        self.enableOnly(Math)
        #self.childs += [MessageView(self, 'hello')]

    def procToken(self, token):
        t2 = token[1]
        if t2 == TType.sf:
            self.sf = not self.sf
        elif t2 == TType.alpha:
            self.alpha = not self.alpha
        elif t2 == TType.mode:
            self.childs[-1].enabled = not self.childs[-1].enabled
        elif t2 == TType.reset:
            self.enableOnly(Math)
            mathCtrl = next(x for x in self.childs if isinstance(x, Math))
            mathCtrl.clearRows()
            if len(mathCtrl.childs) == 0:
                mathCtrl.openInp()
        elif t2 == TType.shutdown:
            self.childs.append(MessageView(
                self, 'Enter password', self._shutdown, MVType.inpField))
        else:
            super().procToken(token)
        if t2 != TType.sf:
            self.sf = False

    def enableOnly(self, childType):
        for c in self.childs:
            c.enabled = isinstance(c, childType)

    def _shutdown(self, s):
        if s == 'pi':  # this is the password
            self.childs.append(View(self, ['Shutting', '        down...']))
            for c in self.childs:
                if isinstance(c, Math):
                    c.procClose()
            f = open(relatPath('../../exit.txt'), mode='w')
            f.write('shutdown')
            f.close()
            ######## MASTER SWITCH OFF ########
            modules.alive = False
        else:
            self.childs.append(View(self, ['Wrong password', 'press back...']))

    def drawChar(self, i):
        if self.sf:
            return CusChar.sf
        elif self.alpha:
            return CusChar.alpha
        else:
            return CusChar.void
