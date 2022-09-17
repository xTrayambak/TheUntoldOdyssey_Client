#!/usr/bin/env python3
from src.client.settingsreader import get_setting
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

        self.STR_TO_FUNC = {
            "fps_toggle": instance.toggle_fps_counter,
            "wireframe_toggle": instance.toggle_wireframe,
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
        keybinds = get_setting("keybinds")
        for function in keybinds:
            key = keybinds[function]
            log(f"Binding function '{function}' to key '{key}'")
            self.events.update({key: []})

            self.listen_for(key)

    def hook_key(self, key, func = None):
        self.events[key].append(func)

    def listen_for(self, key):
        def pseudofunc():
            for func in self.events[key]:
                try: func()
                except Exception as exc: raise exc

        self.instance.accept(key, pseudofunc)

    def hook(self):
        log("Hooking input system into TUO process.", "Worker/InputManager")

        _keybinds = get_setting("keybinds")

        for _func in _keybinds:
            if _func in self.STR_TO_FUNC:
                func = self.STR_TO_FUNC[_func]
                key = _keybinds[_func]
                self.hook_key(key, func)
