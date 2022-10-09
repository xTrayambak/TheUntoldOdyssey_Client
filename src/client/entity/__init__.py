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
from src.client.types.vector import Vector3, derive

from src.log import log, warn


class Entity:
    def __init__(self, instance, name: str, model: str, position: Vector3, hpr: Vector3 = None):
        self.name = name
        self.model = Object(instance, model)
        self.animations = {}
        self.actor = Actor(models = self.model.model)
        self.instance = instance
        self.shaders = {}
        self.position = derive(position)

        # TODO This is a bad way of doing this and wastes unnecessary resources but I am too lazy to find a proper fix right now.
        self.model.destroy()

        if hpr:
            self.hpr = hpr
        else:
            self.hpr = Vector3(0, 0, 0)

        self.shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.node = BulletRigidBodyNode('entity_collision_{}'.format(name))
        self.node.addShape(self.shape)

        self.path = instance.render.attachNewNode(self.node)

        self.actor.reparentTo(self.instance.render)

    def set_texture(self, name: str):
        self.actor.set_texture(
            self.instance.texture_loader.load_texture(name)
        )

    def set_pos(self, position: list | Vector3):
        self.position = position

        if isinstance(position, list) or isinstance(position, tuple):
            self.node.setPos(LVecBase3(position[0], position[1], position[2]))
            self.actor.setPos(LVecBase3(position[0], position[1], position[2]))
        elif isinstance(position, Vector3):
            self.actor.setPos(LVecBase3(position.x, position.y, position.z))

    def get_pos(self) -> Vector3:
        return self.position

    def set_hpr(self, hpr: Vector3):
        self.hpr = hpr
        self.actor.setHpr(LVecBase3(hpr.x, hpr.y, hpr.z))

    def get_hpr(self) -> Vector3:
        return self.hpr

    def play_animation(self, name):
        self.actor.play(name)

    def on_death(self):
        log("Entity has died.")
