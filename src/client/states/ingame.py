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
from src.log import log, warn

process = psutil.Process()

def inGameState(instance, previous_state: int = 1):
    instance.clear()
    instance.game = Game(instance, 0)
    instance.set_fov(getSetting("video", "fov"))
    shaders = loadAllShaders()
    for _shd in shaders:
        instance.workspace.objects["shaders"].append(_shd)
    log("The player is in-game now.")

    #instance.mapLoader.load()

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
    instance.player.init()

    player = instance.player

    ## GUI ##

    ## PUT HUD HERE ##

    ## PUT DEBUG UI HERE ##

    tuo_version = Text(instance, font, text=f"The Untold Odyssey {instance.version}", scale=0.05, alignment=TextNode.ALeft, position=(-1, 0, 0.8))
    debug_stats_world = Text(instance, font, f"E: 0", scale=0.05, position=(-1, 0, 0.6), alignment=TextNode.ALeft)
    memory_stats = Text(instance, font, f"USE: {int(process.memory_info().rss / (1024*1024))}MB / THRES: {gc.get_threshold()[1]} MB/s", scale=0.1, position=(-1, 0, 0.4), alignment=TextNode.ALeft)
    #network_stats = Text(instance, font, f"LP: {int(instance.networkClient.last_packet_ms)}ms", scale=0.1, position=(-1, 0, 0))
    ## TASKS ##

    async def camera_update_task(task):
        if instance.state != instance.states_enum.INGAME: return task.done
 
        position = player.entity.getPos()

        instance.cam.setPos(
            position[0] - 10, position[1] + 5, position[2]
        )

        return task.cont

    async def debug_menu_update(task):
        if instance.game is not None:
            memory_stats.setText(f"USE: {int(process.memory_info().rss / (1024*1024))} MB")
            #debug_stats_world.setText(f"E: {instance.game.entityManager.entity_count} / D: {int(instance.networkClient.last_packet_ms)}")
            #network_stats.setText(f"LP: {instance.networkClient.last_packet_ms}ms")
        return task.cont

    def settingsPage():
        instance.change_state(2)

    def quit_to_menu():
        instance.quit_to_menu()
        instance.networkClient.last_packet_ms = 0

    paused_text = Text(instance, font, "Game Paused", 0.09, position = (0, 0, 0.5))

    settings_button = Button(instance, "Settings", 0.1, 0.085, pos=(0, 0, -0.38), text_font=font, command=settingsPage)
    return_to_menu_button = Button(instance, "Quit to Menu", 0.1, 0.085, pos=(0, 0, 0), text_font=font, command=quit_to_menu)

    paused_text.hide()
    return_to_menu_button.hide()
    settings_button.hide()

    instance.workspace.add_ui("paused_text", paused_text)
    instance.workspace.add_ui("return_to_menu_button", return_to_menu_button)
    instance.workspace.add_ui("settings_button", settings_button)
    instance.workspace.add_ui("debug_stats_world", debug_stats_world)
    instance.workspace.add_ui("debug_stats_version", tuo_version)
    instance.workspace.add_ui("memory_stats_text", memory_stats)
    #instance.workspace.add_ui("debug_network_stats", network_stats)
    instance.spawnNewTask("debug_menu_update", debug_menu_update)
