from enum import IntEnum
from . import View, TType, InputField


class MVType(IntEnum):
    inpField = 0
    multiResp = 1


class MessageView(View):

    def __init__(self, parent, caption, actions, mvtype=MVType.multiResp):
        super().__init__(parent, [caption])
        self._mvtype = mvtype
        self._actions = actions
        if mvtype == MVType.inpField:
            self._actions = [('', actions)]
            self.childs.append(InputField(self, self._closing))
        else:
            pass  # TBF

    # procCmd TBF

    def _closing(self, s):
        if self._mvtype == MVType.inpField:
            self._actions[0][1](s)
        else:
            for resp, a in self._actions:
                if resp == s:
                    a()
        self.closeMe()
