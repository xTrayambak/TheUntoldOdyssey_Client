import math

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

from enum import Enum

from src.client.entity import Entity
from src.client.settingsreader import get_setting
from src.client.types.vector import Vector3, derive

from src.log import log, warn


class MovementStates(Enum):
    WALK = 0
    SPRINT = 1

WalkSpeedForward = {
    MovementStates.WALK: 0.3,
    MovementStates.SPRINT: 0.4
}

WalkSpeedBackward = {
    MovementStates.WALK: 0.2,
    MovementStates.SPRINT: 0.3
}

PeakVelocity = {
    MovementStates.WALK: 0.8,
    MovementStates.SPRINT: 1.5
}

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keymaps = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "sprint": False
        }

        self.movement_velocity = 0.0
        self.accelerating = False
        self.movement_state = MovementStates.WALK
        self.peak_velocity = None

        self.set_texture('assets/textures/terrain/overworld_grass_1.jpg')

        self.instance.new_task('update_ingame', self.update)

        self.instance.accept('w', self.forward)
        self.instance.accept('w-up', self.forward_stop)

        self.instance.accept('a', self.left)
        self.instance.accept('a-up', self.left_stop)

        self.instance.accept('s', self.backward)
        self.instance.accept('s-up', self.backward_stop)

        self.instance.accept('d', self.backward)
        self.instance.accept('d-up', self.backward_stop)

        self.instance.accept('control', self.sprint)

    async def update(self, task):
        if self.instance.get_state() != self.instance.states_enum.INGAME: return task.cont

        self.update_camera()
        self.update_position()
        self.update_rotation()
        return task.cont

    def movement_start(self):
        if self.movement_velocity < 1:
            self.accelerating = True
            self.instance.new_task('bump_vel', self.movement_velocity_bump_task)

    def update_position(self):
        pos = self.get_pos()
        new_pos = derive(pos)

        movement_speed_forward = WalkSpeedForward[self.get_movement_state()]
        movement_speed_backward = WalkSpeedBackward[self.get_movement_state()]

        peak_velocity = PeakVelocity[self.get_movement_state()]

        # FIXME: Fix random movement janks when you release the forward key too fast
        if peak_velocity != self.peak_velocity: self.reset_velocity()

        self.peak_velocity = peak_velocity

        #log(f'Keymaps: {self.keymaps}\nAcceleration State: {self.accelerating}\nMovement Velocity: {self.movement_velocity}\nSprinting: {self.get_movement_state() == MovementStates.SPRINT}')

        # Heading-Pitch-Rotation
        hpr = self.get_hpr()
        log(f'Heading: {hpr.x}\nPitch: {hpr.y}\nRotation: {hpr.z}')

        if self.keymaps['forward']:
            self.movement_start()

            new_x = (new_pos.x + movement_speed_forward) + self.movement_velocity + (hpr.x / 50)
            new_pos.set_pos_elem('x', new_x)

        if self.keymaps['backward']:
            self.movement_start()

            new_x = (new_pos.x - movement_speed_backward) - self.movement_velocity
            new_pos.set_pos_elem('x', new_x)

        if self.keymaps['left']:
            self.movement_start()

        if not self.keymaps['forward'] and not self.keymaps['backward'] and not self.keymaps['left'] and not self.keymaps['right']:
            if self.movement_velocity > 0 and self.accelerating:
                self.accelerating = False
                self.instance.new_task('debump_vel', self.movement_velocity_debump_task)

        self.set_pos(new_pos)


    def update_rotation(self):
        if self.instance.mouseWatcherNode.hasMouse():
            mouse_x = self.instance.mouseWatcherNode.getMouseX()
            mouse_y = self.instance.mouseWatcherNode.getMouseY()


            self.set_hpr(Vector3(
                math.atan2(mouse_y, mouse_x)*59.29578+90+self.instance.camera.getH()
            ))

    def update_camera(self):
        position = self.get_pos()

        # Position the camera to bend down a bit.
        self.instance.camera.set_hpr(
            Vector3(
                0, -20.5, 0
            ).to_lvec3f()
        )

        # Tray teaches:
        # How 2 center ur play3rz camer4 @ da back!!!111111
        # FIXME: Remove these bogus checks sweet heavens these will surely come to bite me in the rear end later on
        if isinstance(position, Vector3):
            self.instance.camera.set_pos(
                Vector3(
                    position.x, position.y - 10, position.z + 5
                ).to_lvec3f()
            )
        elif isinstance(position, list):
            self.instance.camera.set_pos(
                Vector3(
                    position[0], position[1] - 10, position[2] + 5
                ).to_lvec3f()
            )


    def forward(self):
        self.keymaps["forward"] = True

    def forward_stop(self):
        self.keymaps["forward"] = False

    def sprint(self):
        self.keymaps['sprint'] = not self.keymaps['sprint']
        if self.keymaps['sprint']:
            self.set_movement_state(MovementStates.SPRINT)
        else:
            self.set_movement_state(MovementStates.WALK)

    async def movement_velocity_bump_task(self, task):
        if self.movement_velocity >= self.peak_velocity or not self.accelerating: return task.done
        self.movement_velocity += 0.001 * self.instance.getDt()

        await task.pause(0.1)
        return task.cont

    async def movement_velocity_debump_task(self, task):
        if self.movement_velocity <= 0 or self.accelerating:
            self.reset_velocity()
            return task.done

        self.movement_velocity -= 0.1 * self.instance.getDt()

        await task.pause(0.01)

        return task.cont

    def reset_velocity(self):
        self.movement_velocity = 0.0

    def get_movement_state(self) -> MovementStates:
        return self.movement_state

    def set_movement_state(self, flag: MovementStates):
        self.movement_state = flag

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
