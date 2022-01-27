#!/usr/bin/env python3
"""
Managed class for game Workspace.
The workspace is essentially a datatype TUO uses to handle object rendering and hierarchy.
"""

from src.log import *

from panda3d.bullet import BulletDebugNode, BulletWorld
from panda3d.physics import ForceNode, LinearVectorForce

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
        return self.objects["ui"][name]

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

        ## BULLET PHYSICS WORLD ##
        self.world = BulletWorld()

        ## A force node. ##
        self.gravityForceNode = ForceNode("world_client_gravity")
        self.gravityForceNodePath = instance.render.attachNewNode(self.gravityForceNode)

        gravityForce = LinearVectorForce(0, 0, -9.81)

        self.gravityForceNode.addForce(gravityForce)

        instance.physicsMgr.addLinearForce(gravityForce)

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

    def add_object(self, name, obj):
        """
        Add an object to the workspace.
        """
        self.objects.update({name: obj})
        obj.parent = self