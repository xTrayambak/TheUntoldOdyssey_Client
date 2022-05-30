#!/usr/bin/env python3
from src.client.settingsreader import getSetting
from src.log import log, warn

DEFAULT_KEYBINDS = {
    "w": "forward",
    "a": "left",
    "s": "down",
    "d": "right",
    "escape": "quit",
    "backtick": "hide_gui"
}

class InputManager:
    def __init__(self, instance):
        self.events = {

        }

        def wireframe(): 
            if instance.wireframeIsOn:
                instance.wireframeOff()
            else:
                instance.wireframeOn()

            instance.wireframeIsOn = not instance.wireframeIsOn

        def fps_toggle():
            instance.fpsCounterIsOn = not instance.fpsCounterIsOn

            instance.setFrameRateMeter(instance.fpsCounterIsOn)

        self.STR_TO_FUNC = {
            "fps_toggle": fps_toggle,
            "wireframe_toggle": wireframe,
            "freecam": instance.oobe,
            "pause_menu": instance.pause_menu,
            "screenshot": instance.recordingUtil.screenshot,

            ## MOVEMENT ##
            "forward": instance.player.forward,
            "backward": instance.player.backward,
            "left": instance.player.left,
            "right": instance.player.right,

            "forward_stop": instance.player.forward_stop,
            "backward_stop": instance.player.backward_stop,
            "left_stop": instance.player.left_stop,
            "right_stop": instance.player.right_stop,

            "debug_mode": instance.debug_state_secret 
        }

        self.instance = instance

    def init(self):
        keybinds = getSetting("keybinds")
        for function in keybinds:
            key = keybinds[function]
            log(f"Binding function '{function}' to key '{key}'")
            self.events.update({key: []})

            self.listenfor(key)

    def hookkey(self, key, func = None):
        self.events[key].append(func)

    def listenfor(self, key):
        def sudofunc():
            for func in self.events[key]:
                try: func()
                except Exception as exc: warn(f"Unable to execute function for key '{key}' due to error. [{str(exc)}]")

        self.instance.accept(key, sudofunc)

    def hook(self):
        log("Hooking input system into TUO process.", "Worker/InputManager")

        _keybinds = getSetting("keybinds")
        
        for _func in _keybinds:
            if _func in self.STR_TO_FUNC:
                func = self.STR_TO_FUNC[_func]
                key = _keybinds[_func]
                self.hookkey(key, func)