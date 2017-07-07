
from enum import IntEnum
from .helpers import isInt, dec2bin, bin2dec
from .process import Process


class TType(IntEnum):
    text = 0
    func = 1
    sf = 2
    alpha = 3
    opts = 4
    up = 5
    right = 6
    down = 7
    left = 8
    bottom = 9
    reset = 10
    shutdown = 11
    mode = 12
    clear = 13
    esc = 14
    tab = 15
    caps = 16
    shift = 17
    ctrl = 18
    meta = 19
    alt = 20
    space = 21
    enter = 22
    bs = 23
    delete = 24
    copy = 25
    paste = 26
    undo = 27
    redo = 28
    ans = 29
    drg = 30


class CusChar(IntEnum):
    void = 0
    up = 1
    down = 2
    updown = 3
    left = 4
    upleft = 5
    downleft = 6
    udl = 7
    right = 8
    upright = 9
    downright = 10
    udr = 11
    leftright = 12
    ulr = 13
    dlr = 14
    udlr = 15
    sf = 16
    alpha = 17
    shift = 18
    caps = 19

from os import path
relatPath = lambda s: path.join(path.dirname(__file__), s)

alive = True
timeNow = 0
root = None
