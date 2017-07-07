from difflib import SequenceMatcher  # included in std libraries, incredible!
from itertools import product
from . import TType, List, CursorView, InputField, ListMode
from ..parser import parseNotes
import math

titles, tags, notes = zip(*parseNotes())  # unzip
titlesTkns = [x.split() for x in titles]

nlen = len(titles)


class Notes(List):

    def __init__(self, parent):
        super().__init__(
            parent, [('Type query:', lambda: None)], ListMode.fixNum)
        self.childs.append(InputField(self, self._search))
        self._canClose = False
        self.defActList = list(zip(titles, [lambda x=x: self.childs.append(
            CursorView(self, notes[x])) for x in range(nlen)]))

    def _search(self, s):
        #print('searching')
        actList = list(self.defActList)  # copy
        #print(actList)
        if s != '':  # else return all entries in natural order
            tkns = s.split()
            ranks = self._setRanks(tkns, titlesTkns, 4)
            ranks2 = self._setRanks(tkns, tags, 3)
            ranks = [ranks[i] + ranks2[i] for i in range(nlen)]
            #print(ranks)
            # reorder actList by decreasing rank
            idxList = list(zip(*(sorted(zip(ranks, range(nlen)))[::-1])))[1]
            actList = [actList[x] for x in idxList]
        self.updateActList(actList)

    def _setRanks(self, tkns, seq, coeff):
        ranks = [0] * nlen
        for i in range(nlen):
            cp = list(product(tkns, seq[i]))  # cartesian product
            for s1, s2 in cp:
                # try real_quick_ratio
                ranks[i] += coeff * 3 * SequenceMatcher(None, s1, s2).ratio()
                l = min(len(s1), len(s2))
                ranks[
                    i] += coeff * math.log10((len([1 for x in range(l) if s1[x] == s2[x]]) + 1) / l)
        # print(ranks)
        return ranks

    def procCmd(self, t1, t2):
        if t2 in [TType.text, TType.func] and '1' != t1 != '2':
            self.childs.append(InputField(self, self._search))
            self.childs[-1].procToken((t1, t2))  # do not lose the token
        else:
            super().procCmd(t1, t2)
