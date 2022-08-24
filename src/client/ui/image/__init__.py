#!/usr/bin/python3

from panda3d.core import LVecBase3f, LVecBase2f
from direct.gui.OnscreenImage import OnscreenImage

class Image:
    def __init__(self, path: str, pos: tuple | LVecBase2f = None, hpr: tuple | LVecBase3f = None,
            scale: int | float = None, color = None, parent = None
        ):
        self.path = path
        self.pos = pos
        self.hpr = hpr
        self.scale = scale
        self.color = color
        self.parent = parent

        self.direct = OnscreenImage(path, pos, hpr, scale, color, parent)

    def destroy(self):
        return self.direct.destroy()

    def set_scale(self, value: int | float):
        self.direct.set_scale(value)

    def set_image(self, path: str):
        self.path = path

        # Seems there is no good way to set the texture, so we gotta do it the bad way.
        self.destroy()
        self.direct = OnscreenImage(path, self.pos, self.hpr, self.scale, self.color, self.parent)

    def set_hpr(self, value: tuple | LVecBase3f):
        self.direct.set_hpr(value)
