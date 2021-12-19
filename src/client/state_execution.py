#!/usr/bin/env python3
"""
Managed module to handle all client states.
"""
import json
import sys
import gc
import random

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.task import Task

from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, AmbientLight, ClockObject, LVecBase3

from src.client.loader import getAsset, getAllFromCategory
from src.client.log import log
from src.client.shaderutil import loadAllShaders
from src.client.settingsreader import getSetting

from pyglet.gl import gl_info as gpu_info
from math import sin

SIN_VAL_DIV = 20
SIN_VAL_AFTER_DIV = 15

def quitting(instance):
    instance.quit()
    #instance.state = GameStates.LOADING
    gc.collect()
    sys.exit()

def loadingScreen(instance):
    instance.clear()
    #instance.state = GameStates.LOADING
    
    card_syntax_logo = CardMaker("syntaxLogo")
    card = instance.render2d.attachNewNode(card_syntax_logo)

    syntax_logo_texture = instance.loader.loadTexture(getAsset("images", "syntax_logo_default"))
    card.setTexture(syntax_logo_texture)

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def connectingPage(instance):
    instance.clear()

    mangabey_font = instance.loader.loadFont(getAsset("fonts", "mangabey"))
    edgegalaxy_font = instance.loader.loadFont(getAsset("fonts", "edgegalaxy"))

    image = random.choice(getAllFromCategory("loading_screen_images"))

    path = image["path"]
    author_name = image["author"]

    background = OnscreenImage(
        image = path, scale = 1,
        parent = instance.render2d,
        pos = (0, 0, 0)
    )

    label_connecting = TextNode(name = "node_text_connect")
    label_connecting.setText(f"Connecting to [{instance.networkClient.connectingTo}]; locating host and establishing connection.")
    label_connecting.setTextColor((0.1,0.1,0.1,1))
    label_connecting.setAlign(TextNode.ACenter)
    label_connecting.setFont(mangabey_font)
    label_connectingNode = instance.aspect2d.attachNewNode(label_connecting)
    label_connectingNode.setScale(0.1)

    label_tuo = TextNode(name = "node_tuo_version")
    label_tuo.setText("TUO "+instance.version)
    label_tuo.setTextColor((0,0,0,1))
    label_tuo.setAlign(TextNode.ALeft)
    label_tuo.setFont(mangabey_font)
    label_tuoNode = instance.aspect2d.attachNewNode(label_tuo)
    label_tuoNode.setScale(0.07)

    label_artist = TextNode(name = "node_artist")
    label_artist.setText(f"@{author_name}")
    label_artist.setTextColor((0,0,0,1))
    label_artist.setAlign(TextNode.ARight)
    label_artist.setFont(mangabey_font)
    label_artistNode = instance.aspect2d.attachNewNode(label_artist)
    label_artistNode.setScale(0.07)

    label_gpu = TextNode(name = "node_text_gpu")
    label_gpu.setText("OpenGL " +gpu_info.get_version())
    label_gpu.setTextColor((0,0,0,1))
    label_gpu.setAlign(TextNode.ALeft)
    label_gpu.setFont(mangabey_font)
    label_gpuNode = instance.aspect2d.attachNewNode(label_gpu)
    label_gpuNode.setScale(0.07)

    label_gpuNode.setPos((-1.9, 0, -0.8))
    label_tuoNode.setPos((-1.9, 0, -0.9))
    label_artistNode.setPos((1.9, 0, -0.9))

    instance.workspace.add_ui("connecting_screen_status", label_connecting)
    instance.workspace.add_ui("gpu_text", label_gpu)
    instance.workspace.add_ui("tuo_ver_text", label_tuo)
    instance.workspace.add_ui("artist_text", label_artist)
    instance.workspace.add_ui("background_connecting_screen", background)


def mainMenu(instance):
    instance.clear()
    SPLASHES = open(
        getAsset("splash_texts", "path")
    ).readlines()
    #instance.state = GameStates.MENU
    log("The player is currently on the main menu.")

    addr, port = getSetting("networking", "proxy")[0]["ip"], getSetting("networking", "proxy")[0]["port"]
    def _cmd_ingame():  instance.networkClient.connect(addr, port, instance)

    #tuoLogo = OnscreenImage(image = getAsset("images", "logo_default"), pos = (0, 0, 0))
    play_button = DirectButton(text = "PLAY",
                                text_scale = 0.1, 
                                pos = (0, 0, 0),
                                command = _cmd_ingame
                                
    )

    splash_screen_text = TextNode(name = "splash_screen_text")
    splash_screen_text.setAlign(TextNode.ACenter)
    spl_txt = random.choice(SPLASHES)
    splash_screen_text.setText(spl_txt)

    spl_scrn_txt_node = instance.render2d.attachNewNode(splash_screen_text)
    spl_scrn_txt_node.setScale(0.08)
    spl_scrn_txt_node.setPos((0.5, 0, 0.5))
    spl_scrn_txt_node.setHpr(LVecBase3(0.5, 0.5, 0.5))

    class Menu:
        elapsed = 0

    Clock = ClockObject()

    def _splsh_txt_pop(task):
        Menu.elapsed += 1
        Clock.tick()
        _SIN_VAL_DIV = SIN_VAL_DIV + (Clock.dt/10)
        sin_Val = clip(
            sin(Menu.elapsed / _SIN_VAL_DIV) / SIN_VAL_AFTER_DIV,
            0,
            1
        )

        try:
            spl_scrn_txt_node.setScale(sin_Val)
        except AssertionError:
            return Task.done
        if instance.state != instance.states_enum.MENU:
            return Task.done
        return Task.cont

    instance.taskMgr.add(_splsh_txt_pop, "splsh_txt_pop")

    

    """
    settings_button = DirectButton(text = "SETTINGS",
                                text_scale = 0.1,
                                pos = (0, 1, 0)
    )

    quit_button = DirectButton(text = "QUIT",
                                text_scale = 0.1,
                                command=instance.quit
    )"""

    ## PACK INTO WORKSPACE HIERARCHY ##
    instance.workspace.add_ui("play_btn", play_button)
    instance.workspace.add_ui("splash_text", spl_scrn_txt_node)
    #instance.workspace.add_ui("settings_btn", settings_button)
    #instance.workspace.add_ui("quit_btn", quit_button)

def endCredits(instance):
    instance.clear()
    log("End credits have started")
    #instance.state = GameStates.END_CREDITS

def inGameState(instance):
    instance.clear()
    #instance.state = GameStates.INGAME
    log("The player is in-game now.")

    """
    Get heightmap, then cast it to the game
    using Panda3D's GeoMipTerrain class.

    TODO: Make it so that heightmap is downloaded from Syntax Studios API everytime the game launches.
    """
    log("Requesting heightmap", "Worker/GeoMipTerrain")
    heightmap_mesh = GeoMipTerrain("overworld_terrain")
    heightmap_mesh.setHeightfield(getAsset("maps", "overworld_map")["path"])
    heightmap_mesh.setBlockSize(32)
    heightmap_mesh.setNear(20)
    heightmap_mesh.setFar(100)
    heightmap_mesh.setFocalPoint(instance.camera)

    root_heightmap = heightmap_mesh.getRoot()
    root_heightmap.setTexture(TextureStage.getDefault(), instance.loader.loadTexture(getAsset("textures", "terrain_grass_1")["path"]))
    root_heightmap.setTexScale(TextureStage.getDefault(), 100)
    root_heightmap.reparentTo(instance.render)
    root_heightmap.setSz(2500)

    heightmap_mesh.generate()
    log("Terrain generated from heightmap!", "Worker/GeoMipTerrain")


    """
    Calculate ambient lighting with shadows,
    using Panda3D's AmbientLight class.
    """
    log("Starting to calculate Ambient Lighting.", "Worker/Lighting")
    lighting = AmbientLight("Lighting")
    lighting.setColor((0.2, 0.2, 0.2, 1))
    lighting_node = instance.render.attachNewNode(lighting)
    instance.render.setLight(lighting_node)
    instance.workspace.services["lighting"] = {"object": lighting, "node": lighting_node}
    log("Ambient light calculated and binded to Workspace.services!")

    """
    Apply visual shaders
    using Panda3D's built-in shader pipeline.
    """
    shaders = loadAllShaders()
    for _shd in shaders:
        instance.workspace.objects["shaders"].append(_shd)

    