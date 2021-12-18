#!/usr/bin/env python3
"""
Managed class for game Workspace.
The workspace is essentially a datatype TUO uses to handle object rendering and hierarchy.
"""

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
        self.objects["parts"].update({name: object})
        return self.objects["ui"][name]

    def add_ui(self, name, object):
        self.objects["ui"].update({name: object})
        return self.objects["ui"][name]

    def init(self, instance):
        self.instance = instance

    def add_shader(self, object, shader: str):
        if object in self.objects["parts"]:
            for _shader in self.objects["shaders"]:
                name = _shader["name"]
                if name == shader:
                    object.setShader(_shader)

    def getComponent(self, category, name):
        return self.objects[category][name]

    def add_object(self, name, obj):
        self.objects.update({name: obj})
        obj.parent = self