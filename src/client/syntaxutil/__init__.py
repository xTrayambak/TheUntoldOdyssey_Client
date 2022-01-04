import psutil
import gc
from direct.task import Task

from src.client.log import log, warn
from src.client.syntaxutil.tuoexceptions import OutOfMemoryError, OpenGLError

### I have absolutely no clue why the heck I need to divide the bytes by this voodoo doll number, but hey, atleast it works.
MEM_CONVERSION_FACTOR = 1048576

class SyntaxUtil:
    def __init__(self, instance):
        self.instance = instance
        self.process = psutil.Process()

    def hook(self):
        self.instance.spawnNewTask("syntaxutil_memcheck", self.memoryCheck)

    async def memoryCheck(self, task):
        memory_usage = self.process.memory_info().rss / (1024 * 1024)
        max_mem = self.instance.max_mem

        used = memory_usage - max_mem

        if used >= max_mem - 25:
            gc.collect()
            warn(f"The game is using more than [50%] of the memory allocated! ({used}MB/{max_mem}MB)")

        if used >= max_mem - 5:
            warn(f"Game has run out of memory. {used} MB has been used, did the garbage collection fail?")
            raise OutOfMemoryError(f"Too much memory used! SyntaxUtil has shut down the game. ({int(used)}MB/{max_mem}MB)")

        return Task.cont