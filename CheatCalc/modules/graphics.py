from RPi.GPIO import BOARD
from .RPLCD import CharLCD, CursorMode
# splash screen
lcd = CharLCD(pin_rs=40, pin_rw=None, pin_e=37, pins_data=[
    38, 36, 35, 33], numbering_mode=BOARD, cols=16, rows=2, dotsize=8, auto_linebreaks=True)
lcd.write_string('CheatCalc 1.0   ' + '      loading...')

from .RPLCD import cursor as provCur  # provisional cursor


from .parser import parseCusChars
from . import CusChar

customChars = parseCusChars()
for lcdIdx in range(8):
    lcd.create_char(lcdIdx, customChars[lcdIdx][1])


lcdWidth = 16
lcdHeight = 2

screen = [' '] * 32  # char or CusChar
_oldScreen = [' '] * 32

cursor = (0, 0)
_oldCursor = (0, 0)

cursorEnabled = False
_oldCurEnab = False

# there are only 8 slot for custom chars in the lcd
_lcdCusChars = [x for x in CusChar][:8]
_ccLen = len(customChars)


def draw():
    global _oldScreen, _oldCurEnab, cursorEnabled
    for i in range(32):
        if screen[i] != _oldScreen[i]:
            with provCur(lcd, i // 16, i % 16):  # (y, x)
                if not isinstance(screen[i], CusChar):
                    lcd.write_string(screen[i])
                else:
                    # change the first currently unused slot
                    if not screen[i] in _lcdCusChars:
                        idx = next(y for y in range(8) if not _lcdCusChars[y] in [
                            screen[x] for x in range(32) if isinstance(screen[x], CusChar)])
                        lcd.create_char(idx, customChars[next(x for x in range(
                            _ccLen) if customChars[x][0] == screen[i])][1])
                        _lcdCusChars[idx] = screen[i]
                    lcd.write_string(chr(_lcdCusChars.index(screen[i])))
            _oldScreen[i] = screen[i]
    if cursorEnabled != _oldCurEnab:
        lcd.cursor_mode = CursorMode.blink if cursorEnabled else CursorMode.hide
        _oldCurEnab = cursorEnabled
    if cursorEnabled:
        lcd.cursor_pos = (cursor[1], cursor[0])
    cursorEnabled = False


def clear():
    lcd.clear()


def close():
    lcd.close()

