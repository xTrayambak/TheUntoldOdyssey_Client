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

wireframe_on = False

class InputManager:
    def __init__(self):
        pass

    def hook(self, instance):
        log("Hooking input system into TUO process.", "Worker/InputManager")

        def wireframe(): 
            if instance.wireframeIsOn:
                instance.wireframeIsOn = False
                instance.wireframeOff()
            else:
                instance.wireframeIsOn = True
                instance.wireframeOn()

        instance.accept(QUIT_KEY, instance.quit)
        instance.accept(WIREFRAME_KEY, wireframe)
        