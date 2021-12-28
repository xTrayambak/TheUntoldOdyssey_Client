#!/usr/bin/env python3
"""
Managed class for Actors/Entites, objects that can rotate in "weird" ways and move frequently
without killing the CPU. 

Also, Navmesh time!!! :-D
"""

from direct.actor.Actor import Actor
from random import randint

from src.client.loader import getAsset

class Entity:
    def __init__(self, name, instance, model):
        self.name = name
        self.model = getAsset("models", "entities")[model]["path"]
        self.animations = {}
        self.actor = Actor(models = self.model)
        self.instance = instance

        self.shaders = {}

        self.actor.reparentTo(self.instance.render)

    def load_animation(self, name:str, type: str):
        self.animations.update({name: getAsset("animations", name)})

    def play_anim(self, name):
        self.actor.play()