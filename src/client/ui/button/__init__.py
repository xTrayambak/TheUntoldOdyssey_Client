from direct.gui.DirectButton import DirectButton
from direct.gui import DirectGuiGlobals as DGG

class Button():
    def __init__(self, instance, text: str, scale: float = 0.1, text_scale: float = 0.1, pos = (0, 0, 0), command = None, text_font = None, parent = None) -> None:
        self.text = text
        def command_extra():
            instance.narrator.say(f"button click {self.text}")
            if command != None: command()

        self.direct = DirectButton(
            text = text,
            text_scale = text_scale,
            pos = pos,
            command = command_extra,
            text_font = text_font,
            parent = parent
        )
        self.instance = instance

        self.direct.bind(DGG.ENTER, self.on_hover)

    def destroy(self):
        self.direct.destroy()

    def setText(self, text: str):
        self.text = text
        self.direct.setText(text)

    def hide(self):
        self.direct.node().setActive(0)

    def show(self):
        self.direct.node().setActive(1)

    def on_hover(self, args) -> None:
        self.instance.narrator.say(self.text)