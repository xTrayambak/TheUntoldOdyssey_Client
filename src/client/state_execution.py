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

from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, AmbientLight

from src.client.loader import getAsset, getAllFromCategory
from src.client.log import log
from src.client.shaderutil import loadAllShaders

from pyglet.gl import gl_info as gpu_info

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

def connectingPage(instance):
    instance.clear()

    mangabey_font = instance.loader.loadFont(getAsset("fonts", "mangabey"))

    image = random.choice(getAllFromCategory("loading_screen_images"))

    background = OnscreenImage(
        image = image, scale = 1,
        parent = instance.render2d,
        pos = (0, 0, 0)
    )

    label_connecting = TextNode(name = "node_text_connect")
    label_connecting.setText(f"Connecting to [{instance.networkClient.connectingTo}]; locating host and establishing connection.")
    label_connecting.setTextColor((0,0,0,1))
    label_connecting.setAlign(TextNode.ACenter)
    label_connectingNode = instance.aspect2d.attachNewNode(label_connecting)
    label_connectingNode.setScale(0.07)

    label_tuo = TextNode(name = "node_tuo_version")
    label_tuo.setText("TUO "+instance.version)
    label_tuo.setTextColor((0,0,0,1))
    label_tuo.setAlign(TextNode.ALeft)
    label_tuo.setFont(mangabey_font)
    label_tuoNode = instance.aspect2d.attachNewNode(label_tuo)
    label_tuoNode.setScale(0.07)

    label_gpu = TextNode(name = "node_text_gpu")
    label_gpu.setText("OpenGL " +gpu_info.get_version())
    label_gpu.setTextColor((0,0,0,1))
    label_gpu.setAlign(TextNode.ALeft)
    label_gpu.setFont(mangabey_font)
    label_gpuNode = instance.aspect2d.attachNewNode(label_gpu)
    label_gpuNode.setScale(0.07)

    label_gpuNode.setPos((-1.9, 0, -0.8))
    label_tuoNode.setPos((-1.9, 0, -0.9))

    instance.workspace.add_ui("connecting_screen_status", label_connecting)
    instance.workspace.add_ui("gpu_text", label_gpu)
    instance.workspace.add_ui("tuo_ver_text", label_tuo)
    instance.workspace.add_ui("background_connecting_screen", background)


def mainMenu(instance):
    instance.clear()
    #instance.state = GameStates.MENU
    log("The player is currently on the main menu.")

    def _cmd_ingame():  instance.networkClient.connect("www.google.com", 80, instance)

    #tuoLogo = OnscreenImage(image = getAsset("images", "logo_default"), pos = (0, 0, 0))
    play_button = DirectButton(text = "PLAY",
                                text_scale = 0.1, 
                                pos = (0, 0, 0),
                                command = _cmd_ingame
                                
    )

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

    