from panda3d.core import NodePath, LVecBase3f

from src.client.types.vector import Vector3
from src.log import log, warn

class Camera:
    """
    A soft abstraction around direct.showbase.ShowBase's camera.
    """
    def __init__(self, tuo):
        self.tuo = tuo
        self.cam = tuo.camera
        self.np = NodePath()


    def set_hpr(self, hpr: Vector3):
        """
        Set the HPR (heading, pitch, rotation) of the camera.
        """
        if isinstance(hpr, Vector3):
            self.cam.setHpr([hpr.x, hpr.y, hpr.z])
        else:
            warn(f'Camera.set_hpr() expects Vector3, got {type(hpr)}. Attempting to handle situation.', 'Worker/Camera')
            if isinstance(hpr, tuple):
                self.cam.setHpr((hpr[0], hpr[1], hpr[2]))
            elif isinstance(hpr, list):
                self.cam.setHpr((hpr[0], hpr[1], hpr[2]))
            else:
                raise TypeError(
                    'Received HPR as a type that is neither a' +
                    'Vector3, list or tuple. WTF?'
                )


    def set_pos(self, position: Vector3):
        """
        Set the position of the camera.
        """
        if isinstance(position, Vector3):
            self.cam.setPos(LVecBase3f(position.x, position.y, position.z))
        else:
            warn(f'Camera.set_pos() expects Vector3, got {type(position)}. Attempting to handle situation.', 'Worker/Camera')
            if isinstance(position, tuple):
                self.cam.setPos(position)
            elif isinstance(position, list):
                self.cam.setPos((position[0], position[1], position[2]))
            else:
                raise TypeError(
                    'Received position as a type that is neither a',
                    'Vector3, tuple or list. WTF?'
                )


    def get_hpr(self) -> Vector3:
        """
        Get the HPR (heading, pitch, rotation) of the camera.
        """
        return Vector3(
            self.cam.getHpr()[0],
            self.cam.getHpr()[1],
            self.cam.getHpr()[2]
        )


    def get_parent(self) -> NodePath:
        return self.tuo.render

    def getParent(self) -> NodePath:
        return self.get_parent()


    def get_mat(self):
        return 0.0

    def getMat(self):
        return self.get_mat()


    def get_pos(self) -> Vector3:
        """
        Get the position of the camera.
        """
        return Vector3(
            self.cam.getHpr()[0],
            self.cam.getHpr()[1],
            self.cam.getHpr()[2]
        )
