#!/usr/bin/env python

import math
import sys

from panda3d.core import LVecBase3f, LVecBase2f

v3d_l = None
v2d_l = None

v3d_mag = None
v2d_mag = None

if sys.platform in ('win32', 'win64'):
    from src.nimc.nt import optMath
    v3d_l = optMath.vector3DLength
    v2d_l = optMath.vector2DLength

    v3d_mag = optMath.vector3DMagnitude
    v2d_mag = optMath.vector2DMagnitude
elif sys.platform in ('linux', 'darwin'):
    from src.nimc.nix import optMath
    v3d_l = optMath.vector3DLength
    v2d_l = optMath.vector2DLength

    v3d_mag = optMath.vector3DMagnitude
    v2d_mag = optMath.vector2DMagnitude


class Vector3:
    """
    A vector with 3 dimensions.
    """
    def __init__(self,
                 x: float | int = 0,
                 y: float | int = 0,
                 z: float | int = 0
                 ):
        self.x = x
        self.y = y
        self.z = z


    def length(self) -> float | int:
        """
        Get the length of this vector.
        """
        return v3d_l(self.x, self.y, self.z)


    def set_pos_elem(self, key: str, value: float | int):
        if key.lower() == 'x': self.x = value
        if key.lower() == 'y': self.y = value
        if key.lower() == 'z': self.z = value


    def magnitude(self, v2) -> float | int:
        """
        Get the distance between this vector and another.
        """
        return v3d_mag(self.x, self.y, self.z, v2.x, v2.y, v2.z)


    def to_list(self) -> list:
        """
        Convert this vector to a list.
        """
        return [self.x, self.y, self.z]


    def to_tuple(self) -> tuple:
        """
        Convert this vector to a tuple.
        """
        return (self.x, self.y, self.z)


    def to_lvec3f(self):
        """
        Convert this vector to a LVecBase3f
        """
        return LVecBase3f(self.x, self.y, self.z)


class Vector2:
    def __init__(self,
                 x: float | int = 0,
                 y: float | int = 0
                 ):
        self.x = x
        self.y = y


    def length(self) -> float | int:
        return v2d_l(self.x, self.y)


    def magnitude(self, v2) -> float | int:
        return v2d_mag(self.x, self.y, v2.x, v2.y)


    def to_list(self) -> list:
        return [self.x, self.y]


    def to_tuple(self) -> tuple:
        return (self.x, self.y)


    def __str__(self) -> str:
        return '{} {} {}'.format(self.x, self.y, self.z)


def derive(vector: LVecBase2f | LVecBase3f) -> Vector2 | Vector3:
    if isinstance(vector, LVecBase2f):
        return Vector2(vector.x, vector.y)
    elif isinstance(vector, LVecBase3f):
        return Vector3(vector.x, vector.y, vector.z)
    elif isinstance(vector, list) or isinstance(vector, list):
        return Vector3(vector[0], vector[1], vector[2])
    elif isinstance(vector, Vector3): return vector

    raise TypeError('Vector must panda3d.core.LVecBase3f, panda3d.core.LVecBase2f, list or tuple!')
