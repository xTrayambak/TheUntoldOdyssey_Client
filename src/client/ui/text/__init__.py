from panda3d.core import TextNode

import random
import sys
import threading

class Text:
    def __init__(self, instance, font, text: str = "Hello, World!", scale: float = 0.01, position = (0, 0, 0), alignment: any = TextNode.ACenter):
        self.node = TextNode(str(random.randint(-sys.maxsize, sys.maxsize)))
        self.node.setText(text)
        self.node.setAlign(alignment)
        self.node.setFont(font)

        self.text = text

        self.nodePath = instance.aspect2d.attachNewNode(self.node)
        self.nodePath.setPos(position)
        self.nodePath.setScale(scale)

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

    def destroy(self):
        self.nodePath.removeNode()