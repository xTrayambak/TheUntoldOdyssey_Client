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

from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, AmbientLight, ClockObject, LVecBase3, TransparencyAttrib

from src.client.loader import getAsset, getAllFromCategory
from src.client.log import log, warn
from src.client.shaderutil import loadAllShaders
from src.client.settingsreader import getSetting
from src.client.player import Player

from pyglet.gl import gl_info as gpu_info
from math import sin

SIN_VAL_DIV = 15
SIN_VAL_AFTER_DIV = 10

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

    mangabey_font = instance.fontLoader.load("mangabey")


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
    ## Clear all UI. ##
    instance.clear()

    edgegalaxy_font = instance.fontLoader.load("edgegalaxy")
    really_font = instance.fontLoader.load("really")

    ## Get splash texts. ##
    SPLASHES = open(
        getAsset("splash_texts", "path")
    ).readlines()


    log("The player is currently on the main menu.")

    ## Networking stuff ##
    addr, port = getSetting("networking", "proxy")[0]["ip"], getSetting("networking", "proxy")[0]["port"]
    def _cmd_ingame():  
        #instance.networkClient.connect(instance, addr, port)
        #instance.networkClient.send({"action": "authenticate","username": "xTrayambak", "password": "joemama123"})
        instance.change_state(3)
    
    ## UI stuff. ##
    _card = CardMaker("tuoLogo")
    card = instance.render2d.attachNewNode(_card.generate())

    tuoLogo_tex = instance.loader.loadTexture(getAsset("images", "logo_default"))
    card.setTexture(tuoLogo_tex)
    card.setScale(0.5)
    card.setPos((-0.2, 0, 0.3))

    play_button = DirectButton(text = "PLAY",
                                text_scale = 0.1, 
                                pos = (0, 0, 0),
                                command = _cmd_ingame,
                                text0_font = really_font
    )

    splash_screen_text = TextNode(name = "splash_screen_text")
    splash_screen_text.setAlign(TextNode.ACenter)
    spl_txt = random.choice(SPLASHES)
    splash_screen_text.setText(spl_txt)
    splash_screen_text.setFont(edgegalaxy_font)

    spl_scrn_txt_node = instance.render2d.attachNewNode(splash_screen_text)
    spl_scrn_txt_node.setScale(0.08)
    spl_scrn_txt_node.setPos((0.5, 0, 0.5))
    spl_scrn_txt_node.setHpr(LVecBase3(5.5, 0, 5.5))

    class Menu:
        elapsed = 0

    Clock = ClockObject()

    def _splsh_txt_pop(task):
        Menu.elapsed += 1
        Clock.tick()
        _SIN_VAL_DIV = SIN_VAL_DIV + (Clock.dt/15)
        sin_Val = clip(
            sin(Menu.elapsed / _SIN_VAL_DIV) / SIN_VAL_AFTER_DIV,
            0.04,
            1
        )

        try:
            spl_scrn_txt_node.setScale(sin_Val)
        except AssertionError:
            return Task.done

        if instance.state != instance.states_enum.MENU:
            return Task.done

        return Task.cont

    instance.spawnNewTask("splsh_txt_pop", _splsh_txt_pop)

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
    instance.workspace.add_ui("tuoLogo", card)
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


    instance.globalClock.setMode(ClockObject.MNormal)
    instance.globalClock.setFrameRate(120)

    instance.set_background_color((0, 255, 245, 1))

    """
    Apply visual shaders
    using Panda3D's built-in shader pipeline.
    """
    shaders = loadAllShaders()
    for _shd in shaders:
        instance.workspace.objects["shaders"].append(_shd)

    instance.player = Player(instance, "player", "player")
    instance.player.init()