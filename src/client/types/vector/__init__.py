#!/usr/bin/env python

import math
from panda3d.core import LVecBase3f, LVecBase2f

class Vector3:
    """
    A vector with 3 dimensions.
    """
    def __init__(self,
                 x: float | int,
                 y: float | int,
                 z: float | int
                 ):
        self.x = x
        self.y = y
        self.z = z


    def length(self) -> float | int:
        """
        Get the length of this vector.
        """
        return math.sqrt(
            self.x * self.x,
            self.y * self.y,
            self.z * self.z
        )


    def magnitude(self, v2) -> float | int:
        """
        Get the distance between this vector and another.
        """
        x1 = self.x
        x2 = v2.x

        y1 = self.y
        y2 = v2.y

        z1 = self.z
        z2 = v2.z

        x = (x1 - x2)
        y = (y1 - y2)
        z = (z1 - z2)

        f = math.sqrt(
            (x * x) + (y * y) + (z * z)
        )

        # Someone told me to not fuck with the GC's work.
        # Did I listen? No.
        del x1
        del x2
        del y1
        del y2
        del z1
        del z2
        del x
        del y
        del z

        return f


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


class Vector2:
    def __init__(self,
                 x: float | int,
                 y: float | int
                 ):
        self.x = x
        self.y = y


    def length(self) -> float | int:
        return math.sqrt(
            self.x * self.x + self.y * self.y
        )


    def magnitude(self, v2) -> float | int:
        dx = (self.x - v2.x)
        dy = (self.y - v2.y)

        return math.sqrt(dx * dx + dy * dy)


    def to_list(self) -> list:
        return [self.x, self.y]


    def to_tuple(self) -> tuple:
        return (self.x, self.y)


def derive(vector: LVecBase2f | LVecBase3f) -> Vector2 | Vector3:
    if isinstance(vector, LVecBase2f):
        return Vector2(vector.x, vector.y)
    elif isinstance(vector, LVecBase3f):
        return Vector3(vector.x, vector.y, vector.z)

    raise TypeError('Vector must panda3d.core.LVecBase3f or panda3d.core.LVecBase2f!')
