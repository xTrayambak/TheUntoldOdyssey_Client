from src.client.log import log

DEFAULT_KEYBINDS = {
    "w": "forward",
    "a": "left",
    "s": "down",
    "d": "right",
    "escape": "quit",
    "backtick": "hide_gui"
}

class InputManager:
    def __init__(self):
        pass

    def hook(self, instance):
        log("Hooking input system into TUO process.", "Worker/InputManager")
        instance.accept("escape", instance.quit)

        