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
from src.client.util.conversion import encode

from src.client.loader import getAsset, getAllFromCategory
from src.log import log, warn
from src.client.shaderutil import loadAllShaders
from src.client.settingsreader import *
from src.client.objects import Object
from src.client.tasks import *

from src.client.ui.button import Button
from src.client.ui.text import Text

from math import sin, pi

def inGameState(instance, previous_state: int = 1):
    instance.clear()
    #instance.state = GameStates.INGAME
    log("The player is in-game now.")

    instance.mapLoader.load()

    basic_font = instance.fontLoader.load("gentium_basic")

    font = basic_font
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

    ## GUI ##

    ## PUT HUD HERE ##

    ## PUT DEBUG UI HERE ##

    #tuo_version = Text(instance, font, f"The Untold Odyssey {instance.version}", 0.05, TextNode.ALeft)
    debug_stats_world = Text(instance, font, f"E: 0 / US: 0", scale=0.1)

    ## TASKS ##

    async def debug_menu_update(task):
        if instance.game is not None:
            debug_stats_world.setText(f"E: {instance.game.entityManager.entity_count}")
        return task.cont

    def settingsPage():
        instance.change_state(2)

    paused_text = Text(instance, font, "Game Paused", 0.09, position = (0, 0, 0.5))

    settings_button = Button(instance, "Settings", 0.1, 0.085, pos=(0, 0, -0.38), text_font=font, command=settingsPage)
    return_to_menu_button = Button(instance, "Quit to Menu", 0.1, 0.085, pos=(0, 0, 0), text_font=font, command=instance.quit_to_menu)

    paused_text.hide()
    return_to_menu_button.hide()
    settings_button.hide()

    instance.workspace.add_ui("paused_text", paused_text)
    instance.workspace.add_ui("return_to_menu_button", return_to_menu_button)

    instance.workspace.add_ui("settings_button", settings_button)

    instance.spawnNewTask("debug_menu_update", debug_menu_update)