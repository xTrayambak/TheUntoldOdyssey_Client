#!/usr/bin/env python3
from panda3d.core import Vec3, TransparencyAttrib
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

from src.log import log, warn
from src.client.loader import getAsset

class Object:
    def __init__(self, instance, model: str):
        self.instance = instance
        self.model = instance.objectLoader.loadObject(model)

        self.canCollide = True

        self.model.reparentTo(instance.render)

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