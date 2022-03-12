from panda3d.core import TextNode
from panda3d.core import TextProperties
from panda3d.core import TextPropertiesManager

import random
import sys
import threading

CHARS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
    "t", "u", "v", "x", "y", "z", "/", "-", "=", "+", "<", ">", "{", "}", "_", "/", "(", ")"
    , "*", ";", ":", "&", "^", "%", "$", "#", "@", "!"
]

class TextFormatting:
    JUMBLE = "[J]"
    UNDERLINE = "[U]"
    ITALIC = "[I]"

properties_italic = TextProperties()

tpMgr = TextPropertiesManager.getGlobalPtr()

class Text:
    def __init__(self, instance, font, text: str = "Hello, World!", scale: float = 0.01, position = (0, 0, 0), alignment: any = TextNode.ACenter, parent=None):
        self.node = TextNode(str(random.randint(-sys.maxsize, sys.maxsize)))
        self.node.setText(text)
        self.node.setAlign(alignment)
        self.node.setFont(font)

        self.text = text
        self.parent = None

        self.nodePath = instance.aspect2d.attachNewNode(self.node)
        self.nodePath.setPos(position)
        self.nodePath.setScale(scale)

        self.instance = instance

        self.format()

    def format(self):
        if self.text.startswith(TextFormatting.JUMBLE):
            self.instance.spawnNewTask("jumble-txt-text", self.jumble_task)

    def setHpr(self, position: tuple):
        self.nodePath.setHpr(position)

    def jumble_task(self, task):
        try:
            string = ""
            for x in range(random.randint(4, 9)):
                string += random.choice(CHARS)

            self.setText(
                string
            )

            task.pause(0.5)
            return task.cont
        except:
            return task.done

    def hide(self):
        self.node.setText(" ")
    
    def show(self):
        self.node.setText(self.text)

    def setPos(self, position = (0, 0, 0)):
        self.nodePath.setPos(position)
    
    def setScale(self, scale: float = 0.01):
        self.nodePath.setScale(scale)

    def setText(self, text: str = "Hello, World!"):
        self.node.setText(text)
        self.text = text
        self.format()

    def destroy(self):
        self.nodePath.removeNode()