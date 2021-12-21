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

wireframe_on = False

class InputManager:
    def __init__(self):
        pass

    def hook(self, instance):
        log("Hooking input system into TUO process.", "Worker/InputManager")

        def wireframe(): 
            if instance.wireframeIsOn:
                instance.wireframeOff()
            else:
                instance.wireframeOn()

            instance.wireframeIsOn = not instance.wireframeIsOn

        def fps_toggle():
            instance.fpsCounterIsOn = not instance.fpsCounterIsOn

            instance.setFrameRateMeter(instance.fpsCounterIsOn)

        instance.accept(QUIT_KEY, instance.quit)
        instance.accept(WIREFRAME_KEY, wireframe)
        instance.accept(FPS_TOGGLE, fps_toggle)