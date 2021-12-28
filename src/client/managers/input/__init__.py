#!/usr/bin/env python3
from src.client.log import log
from src.client.settingsreader import getSetting

DEFAULT_KEYBINDS = {
    "w": "forward",
    "a": "left",
    "s": "down",
    "d": "right",
    "escape": "quit",
    "backtick": "hide_gui"
}

FORWARD_KEY = getSetting("keybinds", "forward")
BACKWARD_KEY = getSetting("keybinds", "backward")
LEFT_KEY = getSetting("keybinds", "left")
RIGHT_KEY = getSetting("keybinds", "right")

QUIT_KEY = getSetting("keybinds", "quit")
WIREFRAME_KEY = getSetting("keybinds", "wireframe_toggle")

FPS_TOGGLE = getSetting("keybinds", "fps_toggle")

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
            "quit": instance.quit,
            "fps_toggle": fps_toggle,
            "wireframe_toggle": wireframe
        }

        self.instance = instance

    def init(self):
        keybinds = getSetting("keybinds")
        for function in keybinds:
            key = keybinds[function]
            log(f"Binding function '{function}' to key '{key}'")
            self.events.update({key: []})

            self.listenfor(key)

    def hookkey(self, key = QUIT_KEY, func = None):
        self.events[key].append(func)
    def listenfor(self, key):
        def sudofunc():
            for func in self.events[key]:
                func()

        self.instance.accept(key, sudofunc)

    def hook(self):
        log("Hooking input system into TUO process.", "Worker/InputManager")

        _keybinds = getSetting("keybinds")
        
        for _func in _keybinds:
            if _func in self.STR_TO_FUNC:
                func = self.STR_TO_FUNC[_func]
                key = _keybinds[_func]
                self.hookkey(key, func)