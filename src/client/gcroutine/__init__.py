from src.log import log, warn
from src.client.module import Module, ModuleCodes
import gc

class GC(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.enabled = True
        self.delay = 60
        self.name = 'TUO_GC_MANUAL_ROUTINE'

    def set_delay(self, val: float | int):
        if val < 30:
            warn('GC routine pause time has been reduced to a value lesser than 30. The game may become unstable.', 'Worker/GCRoutine')
        self.delay = val

    def tick(self, client):
        log('Collecting unused/unreferenced objects to free up memory.', 'Worker/GCRoutine')
        gc.collect()
        log(f'GC routine ended. Sleeping for {self.delay} seconds.', 'Worker/GCRoutine')

        return (ModuleCodes.TICK_CONTINUE, ModuleCodes.TICK_SUCCESS, ModuleCodes.PAUSE, self.delay)
