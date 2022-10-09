#!/usr/bin/env python3
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3, TransparencyAttrib

from src.client.loader import getAsset
from src.log import log, warn


class Object:
    """
    A soft wrapper around `panda3d.core.NodePath`
    """
    def __init__(self, instance, model: str):
        self.instance = instance
        self.model = instance.objectLoader.load_object(model)

        self.can_collide = True

        self.model.reparentTo(instance.render)


    def destroy(self):
        """
        Destroy this object. Once all pointers to this object are removed and the GC thinks it is not needed, it will be garbage collected automatically.
        """
        self.model.removeNode()


    def reparent_to(self, parent):
        self.model.reparentTo(parent)


    def set_two_sided(self, value: bool):
        self.model.set_two_sided(value)


    def set_hpr(self, vector):
        self.model.setHpr(vector)


    def set_scale(self, scale):
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
        self.can_collide = value


    def set_texture(self, texture: str):
        self.model.setTexture(
            self.instance.texture_loader.load_texture(texture)
        )


    def get_object(self):
        return self.model


    def set_pos(self, position = (0, 0, 0)):
        self.model.setPos(position)
