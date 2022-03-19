import psutil
import gc
import sys
from direct.task import Task
from requests import get

from src.log import log, warn
from src.client.syntaxutil.tuoexceptions import OutOfMemoryError, OpenGLError, AnticheatTrigger
from src.client.shared import DATA_PROVIDER

def percent(up, down):
    """
    I forgor (💀) exact terms of division fraction, so I use up and down.
    """
    return (up / down) * 100

class SyntaxUtil:
    def __init__(self, instance):
        self.instance = instance
        self.process = psutil.Process()

    def hook(self):
        self.instance.spawnNewTask("syntaxutil_memcheck", self.memoryCheck)
        #self.instance.spawnNewTask("syntaxutil_processCheck", self.processCheck)


    async def errorCheckGLSL(self, task):
        pass
    
    async def memoryCheck(self, task):
        await task.pause(5)
        memory_usage = self.process.memory_info().rss / 1048576
        max_mem = self.instance.max_mem

        used = memory_usage - max_mem
        _p = percent(up=used, down=max_mem) * -1

        if _p > 95 and _p < 99:
            gc.collect()
            warn(f"The game is using more than {_p}% of the memory allocated! Attempting to reduce memory usage! ({used}MB/{max_mem}MB)")

        if _p > 99:
            warn(f"Game has run out of memory. {used} MB has been used, did the garbage collection fail?")
            self.instance.quit_to_menu()
            self.instance.quit()
            raise OutOfMemoryError(f"Too much memory used! SyntaxUtil has shut down the game. ({int(used)}MB/{max_mem}MB)")

        return Task.cont