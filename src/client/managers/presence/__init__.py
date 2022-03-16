import pypresence

from src.client.shared import GAMESTATES_TO_STRING, GameStates
from src.log import log, warn
from src.client.loader import getAsset

from direct.task import Task

class RPCManager:
    def __init__(self, instance):
        self.instance = instance
        self.presenceClient = pypresence.Presence('922003305381638144')

    def run(self):
        log("Rich presence started. Binding RPCManager._run to taskManager.", "Worker/RPCManager")
        taskManager = self.instance.taskMgr
        try:
            self.presenceClient.connect()

            taskManager.add(self._run, "run_rpc")
        except:
            warn("RPC Client binding failed.")

    def _run(self, task):
        details = "Playing The Untold Odyssey, a MMORPG-camping experience developed by Syntax Studios!"
        if self.instance.debug_mode:
            details = "Playing The Untold Odyssey, a MMORPG-camping experience developed by Syntax Studios! [DEVELOPER MODE]"
        self.presenceClient.update(
            state = GAMESTATES_TO_STRING[self.instance.state],
            details = details,
            buttons = [
                {"label": "Get the Game for Free!", "url": "https://github.com/xTrayambak/TheUntoldOdyssey_Client/"},
                {"label": "End User License Agreement", "url": getAsset("links", "eula")}
            ],
            large_text = "The Untold Odyssey {}".format(self.instance.version),
            large_image = "tuo_logo"
        )

        return Task.cont