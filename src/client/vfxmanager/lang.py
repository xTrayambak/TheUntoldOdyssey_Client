import math
import random
from panda3d.core import LVecBase3f


def fov_set(instance, fov):
    instance.setFov(int(fov))

    return 0

def cam_shake(instance, shake_type, intensity, duration):
    t_updates_passed = 0

    def _inner(task):
        duration = int(duration)
        if t_updates_passed >= duration:
            return task.done

        t_updates_passed += 1

        def compute_next_shake(pos):
            if shake_type.lower() == 'sine':
                og_sin_val = math.sin(instance.getTimeElapsed())

                # x = sin(t_elapsed)
                # y = intensity_factor
                # z = vec3(x / 0.5, x / 1.5, x / 2.5) * y
                return LVecBase3f(
                    og_sin_val / 0.5,
                    og_sin_val / 1.5,
                    og_sin_val / 2.5
                ) * intensity
            elif shake_type.lower() == 'random':
                return LVecBase3f(
                    random.randint(pos[0] - 5, pos[0] + 5) / intensity,
                    random.randint(pos[1] - 5, pos[1] + 5) / intensity,
                    random.randint(pos[2] - 5, pos[2] + 5) / intensity
                )

        instance.cam.setPos(
            lambda: compute_next_shake(instance.cam.getPos())
        )

        return task.cont

    instance.spawnNewTask('_inner_vfx_shakecam', _inner)

COMMANDS = {
    'fov_set': {'command': fov_set},
    'cam_shake': {'command': print},
    'fade_out': {'command': print}
}