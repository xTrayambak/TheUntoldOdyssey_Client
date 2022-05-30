#!/usr/bin/env python3
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3, TransparencyAttrib

from src.client.loader import getAsset
from src.log import log, warn


class Object:
    """
    A W.I.P replacement to funky NodePath(s).

    WHY WOULD YOU NOT WANT TO USE THESE? INTELLISENSE ACTUALLY WORKS ON THEM UNLIKE `panda3d.core.NodePath` :DD
    """
    def __init__(self, instance, model: str):
        self.instance = instance
        self.model = instance.objectLoader.loadObject(model)

        self.canCollide = True

        self.model.reparentTo(instance.render)

    def reparentTo(self, parent):
        self.model.reparentTo(parent)

    def set_two_sided(self, value: bool):
        self.model.set_two_sided(value)

    def setHpr(self, vector):
        self.model.setHpr(vector)

    def setScale(self, scale):
        self.model.setScale(scale)
    
    def set_compass(self):
        self.model.setCompass()

    def set_light_off(self, value: int = 0):
        self.model.set_light_off(value)

    def set_material_off(self, value: int = 0):
        self.model.set_material_off(value)

    def set_color_off(self, value: int = 0):
        self.model.set_color_off(value)

    def set_bin(self, attribute: str, value: int):
        self.model.set_bin(attribute, value)

    def set_depth_write(self, value: bool):
        self.model.set_depth_write(value)

    def set_collision(self, value: bool):
        self.setCollision(value)

    def setCollision(self, value: bool):
        self.canCollide = value

    def setTexture(self, texture: str):
        self.model.setTexture(
            self.instance.textureLoader.loadTexture(texture)
        )

    def getObject(self):
        return self.model

    def setPos(self, position = (0, 0, 0)):
        self.model.setPos(position)