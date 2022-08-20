from src.log import log
from direct.gui.DirectEntry import DirectEntry

class TextInput:
    def __init__(self, tuo, callback, text: str = '', initialText='', lines: int = 1, focus: int = 1, scale=0.05):
        def enter_event(txt: str):
            if callback != None: callback(txt)

        self.direct = DirectEntry(text = text, scale=scale, command=enter_event, initialText=initialText, numLines=lines, focus=focus)

    def hide(self):
        self.direct.hide()

    def show(self):
        self.direct.show()

    def destroy(self):
        self.direct.destroy()