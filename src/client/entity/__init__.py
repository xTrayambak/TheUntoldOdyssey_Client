#!/usr/bin/env python3
"""
Managed class for Actors/Entites, objects that can rotate in "weird" ways and move frequently
without killing the CPU. 

Also, Navmesh time!!! :-D
"""

from direct.actor.Actor import Actor
from random import randint

from src.log import log, warn

class Entity:
    def __init__(self, name: str, instance, model: str):
        self.name = name
        """self.model = instance.objectLoader.loadObject(
            name = "player", subcategory = "entities"
        )
        self.animations = {}
        self.actor = Actor(models = self.model)"""
        self.instance = instance

        self.shaders = {}

        #self.actor.reparentTo(self.instance.render)

    def set_texture(self, name: str):
        self.model.setTexture(
            self.instance.textureLoader.loadTexture(name)
        )

    def play_anim(self, name):
        self.actor.play(name)

    def onDeath(self):
        log("Entity has died.")