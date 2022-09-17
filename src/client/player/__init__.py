from characterController.PlayerController import PlayerController
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task import Task
from panda3d.bullet import (
    BulletWorld,
    BulletDebugNode,
    BulletPlaneShape,
    BulletBoxShape,
    BulletRigidBodyNode,
    BulletGhostNode,
    BulletTriangleMesh,
    BulletTriangleMeshShape,
    BulletHelper
)
from panda3d.core import Vec3, TransparencyAttrib

from src.client.entity import Entity
from src.client.loader import getAsset
from src.client.settingsreader import get_setting
from src.log import log, warn

MOVEMENT_SPEED = 5 #m/s

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keymaps = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
        }
        self.instance.new_task('update_cam_ingame', self.update)

    async def update(self, task):
        if self.instance.get_state() != self.instance.states_enum.INGAME: return task.done

        self.update_camera()
        return Task.cont

    def update_camera(self):
        position = self.instance.player.get_pos()

        instance.camera.set_pos(
            position[0], position[1], position[2]
        )

    def forward(self):
        self.keymaps["forward"] = True

    def forward_stop(self):
        self.keymaps["forward"] = False

    def left(self):
        self.keymaps["left"] = True

    def left_stop(self):
        self.keymaps["left"] = False

    def right(self):
        self.keymaps["right"] = True

    def right_stop(self):
        self.keymaps["right"] = False

    def backward(self):
        self.keymaps["backward"] = True

    def backward_stop(self):
        self.keymaps["backward"] = False
