from time import perf_counter, sleep
import modules
from modules import graphics
from modules.key_process import procKeysState

graphics.clear()

##### BIG LOOP #####
while modules.alive:
    #print('.')
    modules.timeNow = perf_counter()

    # under certain circumstances root.procCmd() is called twice per cicle,
    # most of the time not at all
    procKeysState()
    modules.root.loop()
    modules.root.draw()  # rendering
    graphics.draw()

    sleep(0.01)  # save as much cpu time as possible to maximize battery life

graphics.close()
