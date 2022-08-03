from src.log import log, warn
from enum import Enum

class ModuleCodes(Enum):
    TICK_SUCCESS = 0
    TICK_FAIL = 1

    TICK_CONTINUE = 2
    TICK_DONE = 3

class Module:
    def __init__(self, name: str):
        self.name = name

    def tick(self, client):
        return (ModuleCodes.TICK_CONTINUE, ModuleCodes.TICK_SUCCESS)
