#!/usr/bin/env python3
"""
Managed class for Actors/Entites, objects that can rotate in "weird" ways and move frequently
without killing the CPU. 

Also, Navmesh time!!! :-D
"""

from direct.actor.Actor import Actor
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import LVecBase3
from panda3d.core import Vec3, TransparencyAttrib
from random import randint

from src.client.objects import Object
from src.log import log, warn


class Entity:
    def __init__(self, instance, name: str, model: str, position: list):
        self.name = name
        self.model = Object(instance, model)
        self.animations = {}
        self.actor = Actor(models = self.model.model)
        self.instance = instance
        self.shaders = {}
        self.position = position

        self.shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.node = BulletRigidBodyNode('entity_collision_{}'.format(name))
        self.node.addShape(self.shape)

        self.path = instance.render.attachNewNode(self.node)

        self.actor.reparentTo(self.instance.render)

    def set_texture(self, name: str):
        self.model.setTexture(
            self.instance.textureLoader.loadTexture(name)
        )

    def set_pos(self, position: list):
        self.position = position
        self.node.setPos(LVecBase3(position[0], position[1], position[2]))
        self.actor.setPos(LVecBase3(position[0], position[1], position[2]))

    def get_pos(self):
        return self.position

    def play_animation(self, name):
        self.actor.play(name)

    def on_death(self):
        log("Entity has died.")
