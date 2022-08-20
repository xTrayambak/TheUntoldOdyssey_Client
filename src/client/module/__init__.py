from src.log import log, warn
from enum import Enum

from direct.task import Task

class ModuleCodes(Enum):
    TICK_SUCCESS = 0
    TICK_FAIL = 1

    TICK_CONTINUE = 2
    TICK_DONE = 3

    PAUSE = 4

class Module:
    def __init__(self, name: str):
        self.name = name

    async def call_task(self, client):
        data = self.tick(client)
        if len(data) > 2:
            do_pause = data[2] == ModuleCodes.PAUSE
            if do_pause:
                await Task.pause(data[3])

        if data[0] == ModuleCodes.TICK_CONTINUE: return Task.cont
        else: return Task.done

    def tick(self, client):
        return (ModuleCodes.TICK_CONTINUE, ModuleCodes.TICK_SUCCESS)
