import _thread
from subprocess import Popen, PIPE, STDOUT


class Process():

    def __init__(self, cmd, outCb):
        self._proc = Popen(cmd, shell=True, stdout=PIPE,
                           stdin=PIPE, stderr=STDOUT)
        self._callback = outCb
        _thread.start_new_thread(self._outLoop, (self._proc.stdout, ))

    def sendInput(self, s):
        self._proc.stdin.write(bytes(s, 'ascii'))
        self._proc.stdin.flush()

    def _outLoop(self, stm):
        while True:
            s = ''
            if stm.readable():
                s = stm.readline().decode('ascii')
            s = s.rstrip()
            if s != '':
                self._callback(s)

    def close(self):
        self._proc.stdin.close()
        self._proc.stdout.close()
        self._proc.kill()
