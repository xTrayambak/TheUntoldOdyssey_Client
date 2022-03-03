#!/usr/bin/env python3
"""
Managed class for game Workspace.
The workspace is essentially a datatype TUO uses to handle object rendering and hierarchy.
"""

from src.log import *

from panda3d.core import NodePath
from panda3d.bullet import BulletDebugNode, BulletWorld
from panda3d.physics import ForceNode, LinearVectorForce

from threading import Thread

class Workspace:
    def __init__(self):
        self.objects = {
            "parts": {},
            "entities": {},
            "ui": {},
            "shaders": []
        }

        self.services = {
            "lighting":  None
        }

        self.instance = None

    def add_mesh(self, name, object):
        """
        Add a 3D mesh to the workspace hierarchy.
        """
        self.objects["parts"].update({name: object})
        return self.objects["parts"][name]

    def add_ui(self, name, object):
        """
        Add UI to the workspace hierarchy.
        """
        self.objects["ui"].update({name: object})
        return self.objects["ui"][name]

    def init(self, instance):
        """
        Initialize the beautiful world (from that, I mean chaotic) of The Untold Odyssey on the client side.
        From now on, we'll track all the entities and other stuff.
        """
        self.instance = instance

        ## A force node. ##
        self.world = BulletWorld()
        self.world.setGravity(
            (0, 0, -9.81)
        )
        instance.spawnNewTask('world-physics-bullet-update', self.world_update)

    async def world_update(self, task):
        dt = self.instance.clock.dt
        self.world.doPhysics(dt, 10, 1.0/180.0)
        return task.cont

    def add_shader(self, object, shader: str):
        """
        Apply a GLSL shader to an object.
        """
        if object in self.objects["parts"]:
            for _shader in self.objects["shaders"]:
                name = _shader["name"]
                if name == shader:
                    object.setShader(_shader)

    def getComponent(self, category, name):
        """
        Get a component from the workspace.
        """
        return self.objects[category][name]

    def clear(self, category: str = "parts"):
        """
        <THREADED>Clears any category inside the workspace hierarchy.

        instance.workspace.clear -> <THREADED>instance.workspace._clear
        """
        thr = Thread(target = self._clear, args = (category,))
        thr.start()

    def _clear(self, category: str = "parts"):
        """
        Destroy every object in the workspace hierarchy, or in other words..

        Let's yeet 'em all idiots, 'cause be no carin'!
        """
        for _object in self.objects[category]:
            if type(self.objects[category]) == dict:
                object = self.objects[category][_object]

                if type(object) == NodePath:
                    object.removeNode()

    def add_object(self, name, obj):
        """
        Add an object to the workspace.
        """
        self.objects.update({name: obj})
        obj.parent = self