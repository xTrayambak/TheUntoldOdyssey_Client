import psutil
import gc
import sys
from direct.task import Task
from requests import get

from src.log import log, warn
from src.client.syntaxutil.tuoexceptions import OutOfMemoryError, OpenGLError, AnticheatTrigger
from src.client.shared import DATA_PROVIDER

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
        memory_usage = self.process.memory_info().rss / (1024 * 1024)
        max_mem = self.instance.max_mem

        used = memory_usage - max_mem

        if used >= max_mem - 25:
            gc.collect()
            warn(f"The game is using more than [{max_mem} - 25] of the memory allocated! ({used}MB/{max_mem}MB)")

        if used >= max_mem - 5:
            warn(f"Game has run out of memory. {used} MB has been used, did the garbage collection fail?")
            raise OutOfMemoryError(f"Too much memory used! SyntaxUtil has shut down the game. ({int(used)}MB/{max_mem}MB)")

        return Task.cont