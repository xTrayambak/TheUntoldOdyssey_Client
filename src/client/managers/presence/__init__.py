import pypresence
import struct

from direct.task import Task

from src.client.loader import getAsset
from src.client.shared import GAMESTATES_TO_STRING, GameStates
from src.log import log, warn


class RPCManager:
    def __init__(self, instance):
        self.instance = instance
        self.presence_client = pypresence.Presence('922003305381638144')

    def run(self):
        log("Rich presence started. Binding RPCManager._run to taskManager.", "Worker/RPCManager")
        try:
            self.presence_client.connect()
            self.instance.new_task('run_discord_rpc', self._run)
        except Exception as exc:
            warn("RPC Client binding failed.", err=exc)

    def _run(self, task):
        details = "Playing The Untold Odyssey, a MMORPG-camping experience developed by Syntax Studios!"

        if self.instance.globals['debug_mode']:
            details += '[DEBUG MODE]'

        try:
            self.presence_client.update(
                state = GAMESTATES_TO_STRING[self.instance.state],
                details = details,
                buttons = [
                    {"label": "Get the game!", "url": "https://github.com/xTrayambak/TheUntoldOdyssey_Client/"},
                    {"label": "End User License Agreement", "url": getAsset("links", "eula")}
                ],
                large_text = "The Untold Odyssey {}".format(self.instance.version),
                large_image = "tuo_logo"
            )
        except struct.error:
            warn('Discord RPC gateway shut down unexpectedly. Crash handled successfully!', 'Worker/DiscordRPC')
            return Task.done

        return Task.cont
