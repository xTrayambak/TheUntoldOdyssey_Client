#!/usr/bin/env python3
from src.log import log, warn
from src.client.loader import getAsset

class Object:
    def __init__(self, instance, model: str = "map"):
        self.instance = instance
        self.model = instance.objectLoader.loadObject(model)

        self.model.reparentTo(instance.render)

    def setTexture(self, texture: str):
        self.model.setTexture(
            self.instance.textureLoader.loadTexture(texture)
        )

    def getObject(self):
        return self.model

    def setPos(self, position = (0, 0, 0)):
        self.model.setPos(position)