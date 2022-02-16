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

def inGameState(instance, previous_state: int = 1):
    instance.clear()
    #instance.state = GameStates.INGAME
    log("The player is in-game now.")

    instance.mapLoader.load()

    """
    Apply visual shaders
    using Panda3D's built-in shader pipeline.
    """
    shaders = loadAllShaders()
    for _shd in shaders:
        instance.workspace.objects["shaders"].append(_shd)

    sunlight = DirectionalLight("sunlight")
    sunlight.setColor((0.8, 0.8, 0.5, 1))

    sunlightNode = instance.render.attachNewNode(sunlight)
    sunlightNode.setHpr(
        LVecBase3(0, -60, 0)
    )
    
    instance.render.setLight(sunlightNode)

    instance.workspace.services["lighting"] = (sunlight, sunlightNode)
    instance.player.init()

    #instance.workspace.add_mesh("skybox", skybox)