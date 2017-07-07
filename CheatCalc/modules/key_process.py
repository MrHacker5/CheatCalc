import RPi.GPIO as io
import modules as m
from .ui import Root
from . import TType
from .parser import parseKeyLayout, parseKeyPins

##### MASTER INIT #####
m.root = Root()

KN, inPins, outPins, ioCodes = parseKeyPins()
keys = parseKeyLayout()

#pressTime = 0
#keyCfmd = True  # key confirmed
#keyAct = False  # ensure one activation per key press
oldKey = -1
lastTime = 0
oldValidKey = -1
actCnt = 0
token = ('', TType.text)
waiting = False

# GPIO setup
# io.setwarnings(False)
io.setmode(io.BOARD)
# io.cleanup()
for i in range(4):
    io.setup(inPins[i], io.IN, pull_up_down=io.PUD_UP)

for i in range(8):
    io.setup(outPins[i], io.OUT)


# this function detect key press based on duration and discard glitches
# then chooses the right token based on timing and key repetition
def procKeysState():
    global oldKey, lastTime, oldValidKey, actCnt, token, waiting
    currkey = -1
    # get physical key
    for k in range(KN):
        iop = ioCodes[k]
        io.output(outPins[iop.OUT], False)
        if not io.input(inPins[iop.IN]):
            currkey = k
        io.output(outPins[iop.OUT], True)
    if currkey != -1:
        if currkey != oldKey:
            if waiting:
                if oldValidKey == currkey:
                    actCnt += 1
                else:
                    m.root.procToken(token)
                    actCnt = 0
                    waiting = False
            mode = 1 if m.root.sf and len(keys[currkey][1]) > 0 else 2 if m.root.alpha and len(
                keys[currkey][2]) > 0 else 0
            l = len(keys[currkey][mode])
            if l > 0:
                token = keys[currkey][mode][actCnt % l]
                if l == 1:
                    m.root.procToken(token)
                else:
                    waiting = True
            oldValidKey = currkey
            lastTime = m.timeNow
    elif waiting and m.timeNow - lastTime > 0.5:
        m.root.procToken(token)
        actCnt = 0
        waiting = False
    oldKey = currkey