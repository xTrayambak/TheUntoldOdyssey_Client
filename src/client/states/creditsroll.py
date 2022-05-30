import gc
import json
import random
import sys
import threading
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.task import Task
from distutils.command.sdist import sdist
from math import sin, pi
from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, DirectionalLight, AmbientLight, \
    ClockObject, LVecBase3, LVecBase4f, TransparencyAttrib, AmbientLight
from time import sleep

from src.client.io import IOFile
from src.client.loader import getAsset, getAllFromCategory
from src.client.objects import Object
from src.client.settingsreader import *
from src.client.shaderutil import loadAllShaders
from src.client.tasks import *
from src.client.ui.button import Button
from src.client.ui.text import Text
from src.log import log, warn


def endCredits(instance, previous_state: int = 1):
    """
    The end credits. Show the credits in the end, duhh.
    """
    instance.clear()
    log("End credits have started")

    end_credits_dialog = IOFile.new('assets/dialogs/credits_scene', 'r').readlines()

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

            if line.isspace():
                delay = 2

            if instance.is_closing(): break
            sleep(int(delay))
        
        if not instance.is_closing():
            instance.ambienceManager.end_credits.stop()
            instance.change_state(previous_state)

    threading.Thread(target = threaded, args = ()).start()
    return 'credits-complete'