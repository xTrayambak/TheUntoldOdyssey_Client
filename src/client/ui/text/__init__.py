import math
import random
import sys
import threading
from panda3d.core import LVecBase4f
from panda3d.core import TextNode
from panda3d.core import TextProperties
from panda3d.core import TextPropertiesManager

from src.libs.noise.perlin import SimplexNoise
from src.log import log, warn

CHARS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
    "t", "u", "v", "x", "y", "z", "/", "-", "=", "+", "<", ">", "{", "}", "_", "/", "(", ")"
    , "*", ";", ":", "&", "^", "%", "$", "#", "@", "!"
]

class TextFormatting:
    JUMBLE = "[J]"
    UNDERLINE = "[U]"
    ITALIC = "[I]"
    BOLD = "[B]"
    SHAKE = "[S]"
    WAVE = "[W]"

def tuple_to_vec4f(tup: tuple):
    return LVecBase4f(*tup)

properties_italic = TextProperties()

tpMgr = TextPropertiesManager.getGlobalPtr()

noiseGen = SimplexNoise()
noiseGen.randomize()
seed = random.randint(-255, 255)

class Text:
    """
    Text Object with special effects.
    """
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
        self.pos = position

        self.format()

    def format(self):
        """
        Check the string for any special effects syntax, then act accordingly.

        TODO: Move this to a thread, else people can create client lagging stuff if this is computationally expensive, but meh, a few if-else statements aren't that bad. (atleast not 20K like YS)
        """
        if self.text.startswith(TextFormatting.JUMBLE):
            self.instance.spawnNewTask("jumble-txt-text", self.jumble_task)
        elif self.text.startswith(TextFormatting.UNDERLINE):
            pass
        elif self.text.startswith(TextFormatting.ITALIC):
            self.setText(self.text.split(TextFormatting.ITALIC)[1])
            self.node.setSlant(0.3)
        elif self.text.startswith(TextFormatting.SHAKE):
            self.setText(self.text.split(TextFormatting.SHAKE)[1])
            self.instance.spawnNewTask("shake-text", self.shake_task)
        elif self.text.startswith(TextFormatting.BOLD):
            self.setText(f"\1black\1{self.get_text().split(TextFormatting.BOLD)[1]}\2\2")
        elif self.text.startswith(TextFormatting.WAVE):
            self.setText(self.text.split(TextFormatting.WAVE)[1])
            self.instance.spawnNewTask('wave-text', self.wave_task)
        elif not self.text.startswith(TextFormatting.ITALIC):
            self.node.setSlant(0)
            

    def setHpr(self, position: tuple):
        """
        Set the "HPR" (heading/yaw, pitch, roll)

        AKA., rotate the text object around.
        """
        self.nodePath.setHpr(position)

    def get_text(self) -> str:
        """
        Get the text of the Text object. (note: if the last `setText` call had `virtual` argument as `True`, then this value may be inaccurate.)
        """
        return self.text

    def shake_task(self, task):
        """
        Text shake effect task.
        Makes the text shake.

        (warning) contains disgusting try-except clause misuse, you may want to cover your eyes from this mess.
        """
        try:
            x, y, z = self.getPos()
            if random.randint(0, 1) == 1:
                pos = (
                    x + random.uniform(0, 0.1),
                    z + random.uniform(0, 0.1)
                )
            else:
                pos = (
                    x - random.uniform(0, 0.1),
                    z - random.uniform(0, 0.1)
                )

            self.setPos(pos, True)
            task.pause(4)
            return task.cont
        except Exception as exc:
            return task.done

    
    def jumble_task(self, task):
        """
        The Text jumbling task.

        Jumbles the text around with random strings generated every 0.5 ms.
        """
        # I learnt this whilst DDLC modding, thanks Dan. ;D
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

    def wave_task(self, task):
        elapsed = self.instance.getFrameTime()
        self.setPos(
            (
                self.getPos('x'),
                0,
                math.sin(elapsed) / 5
            )
        )
        return task.cont

    def hide(self):
        """
        Hide the text, better known as setting the text to nothing. If we delete this object then the `Text.show` function won't work.
        """
        if self.nodePath.is_empty(): return
        self.node.setText(" ")

    def getPos(self, attr: str = None):
        """
        Get the position the Text object is currently at.

        Additionally, you may provide a component attribute name like (x, y, z). Do note, `Y` here will return 0 as in Panda3D `Z` is the vertical offset. And since this Text is 2D, `Y` is always 0.
        """
        if attr:
            if attr.lower() not in ('x', 'y', 'z'):
                raise ValueError("Expected x, y or z for attribute get, got %s".format(attr))

            if attr.lower() == 'x':
                return self.pos[0]
            elif attr.lower() == 'y':
                return self.pos[2]
            elif attr.lower() == 'z':
                return self.pos[1]
        else:
            return self.pos
    
    def show(self):
        if self.nodePath.is_empty(): return
        self.node.setText(self.text)

    def setPos(self, position = (0, 0, 0), virtual: bool = False):
        """
        Set the position of the Text, using a tuple.

        (warning) This uses the Cartesian coordinate system! Values below and beyond -1 and 1 will make the Text go offscreen!
        """
        if self.nodePath.is_empty(): return
        if len(position) < 3:
            # it seems the engine is unhappy until we do this terribleness
            position = (position[0], position[1], 0)

        if not virtual:
            self.pos = position

        self.nodePath.setPos(position)
    
    def setScale(self, scale: float = 0.01):
        """
        Set the scale, in an `int` or `float`.
        """
        if self.nodePath.is_empty(): return
        self.nodePath.setScale(scale)

    def setColor(self, rgb):
        """
        Set the color of the Text object to something.

        If you don't provide it an alpha value, don't worry. It handles it for ya since I am a nice person.
        """
        if self.nodePath.is_empty(): return

        if len(rgb) > 2:
            rgb = (rgb[0], rgb[1], rgb[2], 1.0)

        if isinstance(rgb, tuple):
            self.nodePath.setColor(tuple_to_vec4f(rgb))
        else:
            self.nodePath.setColor(rgb)

    def setText(self, text: str = "Hello, World!"):
        """
        Set the `text` in this Text object to something.
        """
        if self.nodePath.is_empty(): return
        self.node.setText(text)
        self.text = text

        # make sure to update formatting.
        self.format()

    def destroy(self):
        """
        Destroy this object, aka, tell Panda3D to remove it's node from the `render` SceneGraph.
        """
        if self.nodePath.is_empty(): return
        self.nodePath.removeNode()