from direct.gui.DirectButton import DirectButton
from direct.gui import DirectGuiGlobals as DGG

class Button():
    def __init__(self, instance, text: str, text_scale: float = 0.1, pos = (0, 0, 0), command = None, text_font = None) -> None:
        def command_extra():
            instance.narrator.say(f"button click {text}")
            command()

        self.direct = DirectButton(
            text = text,
            text_scale = text_scale,
            pos = pos,
            command = command_extra,
            text_font = text_font
        )

        self.text = text
        self.instance = instance

        self.direct.bind(DGG.ENTER, self.on_hover)

    def destroy(self):
        self.direct.destroy()

    def on_hover(self, args) -> None:
        self.instance.narrator.say(self.text)