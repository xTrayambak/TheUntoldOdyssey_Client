from panda3d.core import TextNode

import random
import sys

class Text:
    def __init__(self, instance, font, text: str = "Hello, World!", scale: float = 0.01, alignment: any = TextNode.ACenter):
        self.node = TextNode(str(random.randint(-sys.maxsize, sys.maxsize)))
        self.node.setText(text)
        self.node.setAlign(alignment)
        self.node.setFont(font)

        self.nodePath = instance.aspect2d.attachNewNode(self.node)
        self.nodePath.setScale(scale)
    
    def setScale(self, scale: float = 0.01):
        self.nodePath.setScale(scale)

    def setText(self, text: str = "Hello, World!"):
        self.node.setText(text)

    def destroy(self):
        self.nodePath.removeNode()