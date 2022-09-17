import gc
import json
import psutil
import random
import sys
import threading
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.task import Task
from distutils.command.sdist import sdist
from math import sin, pi
from panda3d.core import CardMaker, Fog, LVecBase4f, TextNode, GeoMipTerrain, Texture, TextureStage, DirectionalLight, \
    AmbientLight, ClockObject, LVecBase3, LVecBase4f, TransparencyAttrib, AmbientLight
from time import sleep

from src.client.loader import getAsset, getAllFromCategory
from src.client.objects import Object
from src.client.settingsreader import *
from src.client.shaderutil import loadAllShaders
from src.client.tasks import *
from src.client.ui.button import Button
from src.client.ui.text import Text
from src.client.util.conversion import encode
from src.client.visual_shared import *
from src.client.game import Game
from src.client.player import Player
from src.log import log, warn

process = psutil.Process()

def in_game_state(instance, previous_state: int = 1):
    instance.clear()
    instance.set_fov(get_setting("video", "fov"))

    log("The player is in-game now.")

    basic_font = instance.fontLoader.load("gentium_basic")
    font = basic_font

    sunlight = DirectionalLight("sunlight")
    sunlight.setColor((0.8, 0.8, 0.5, 1))

    sunlightNode = instance.render.attachNewNode(sunlight)
    sunlightNode.setHpr(
        LVecBase3(0, -60, 0)
    )
    instance.render.setLight(sunlightNode)
    instance.workspace.services["lighting"] = (sunlight, sunlightNode)

    paused_text = Text(instance, font, "Game Paused", 0.09, position = (0, 0, 0.5))
    settings_button = Button(instance, "Settings", 0.1, 0.085, pos=(0, 0, -0.38), text_font=font, command=lambda: instance.change_state(2))
    return_to_menu_button = Button(instance, "Quit to Menu", 0.1, 0.085, pos=(0, 0, 0), text_font=font, command=lambda: instance.change_state(1))

    paused_text.hide()
    return_to_menu_button.hide()
    settings_button.hide()

    instance.workspace.add_ui("paused_text", paused_text)
    instance.workspace.add_ui("return_to_menu_button", return_to_menu_button)
    instance.workspace.add_ui("settings_button", settings_button)
