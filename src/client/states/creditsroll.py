from distutils.command.sdist import sdist
import json
import sys
import gc
import random
import threading
from time import sleep

from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals as DGG
from direct.task import Task

from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, DirectionalLight, AmbientLight, ClockObject, LVecBase3, LVecBase4f, TransparencyAttrib, AmbientLight

from src.client.loader import getAsset, getAllFromCategory
from src.log import log, warn
from src.client.shaderutil import loadAllShaders
from src.client.settingsreader import *
from src.client.objects import Object
from src.client.tasks import *

from src.client.ui.button import Button
from src.client.ui.text import Text

from pyglet.gl import gl_info as gpu_info
from math import sin, pi

def endCredits(instance, previous_state: int = 1):
    """
    The end credits. Show the credits in the end, duhh.
    """
    instance.clear()
    log("End credits have started")

    end_credits_dialog = open(
            getAsset("dialogs", "end_credits")["path"]
        ).readlines()

    rondalFont = instance.fontLoader.load("rondal")

    dialogText = Text(instance=instance, text="", scale=0.1, font = rondalFont)

    instance.workspace.add_ui("dialogText", dialogText)

    def threaded():
        for line in end_credits_dialog:
            dialogText.setText(line.split("\n")[0].format(instance.player.name))

            length = len(line)


            delay = (
                length // 8
            )

            print(delay)
            sleep(int(delay))
        
        instance.ambienceManager.end_credits.stop()
        instance.change_state(previous_state)

    threading.Thread(target = threaded, args = ()).start()
    return 'credits-complete'