from direct.task.Task import Task
from math import sin
import limeade

from src.log import log

SIN_VAL_DIV = 1
SIN_VAL_AFTER_DIV = 16

def splash_screen_pop(task, instance, spl_scrn_txt_node, clipFunc):
    limeade.refresh()
    _SIN_VAL_DIV = SIN_VAL_DIV + (instance.clock.dt/15)
    sin_Val = clipFunc(
        sin((instance.getFrameTime() / _SIN_VAL_DIV) * 16) / SIN_VAL_AFTER_DIV,
        0.05,
        0.8
    )

    try:
        spl_scrn_txt_node.setScale(sin_Val)
    except AssertionError:
        return Task.done
    except AttributeError:
        return Task.done

    if instance.state != instance.states_enum.MENU:
        return Task.done

    return Task.cont

