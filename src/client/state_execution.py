#!/usr/bin/env python3
"""
Managed module to handle all client states.
"""
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
from math import sin

SIN_VAL_DIV = 15
SIN_VAL_AFTER_DIV = 10

def quitting(instance, previous_state: int = 1):
    instance.quit()
    #instance.state = GameStates.LOADING
    gc.collect()
    sys.exit()

def loadingScreen(instance, previous_state: int = 1):
    instance.clear()
    #instance.state = GameStates.LOADING
    
    card_syntax_logo = CardMaker("syntaxLogo")
    card = instance.render2d.attachNewNode(card_syntax_logo)

    syntax_logo_texture = instance.loader.loadTexture(getAsset("images", "syntax_logo_default"))
    card.setTexture(syntax_logo_texture)

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

class Menu:
    elapsed = 0

def connectingPage(instance, previous_state: int = 1):
    """
    The "connecting to servers, please wait" page.

    (Arima your art is amazing xddddd)
    """
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

    def back_cmd():
        instance.change_state(1)

    back_button = Button(
        text = "Back", pos = (0, 0, -0.4),
        scale = 1,
        instance = instance,
        command = back_cmd
    )

    back_button.hide()

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

    instance.workspace.add_ui("connecting_screen_status", label_connectingNode)
    instance.workspace.add_ui("gpu_text", label_gpuNode)
    instance.workspace.add_ui("tuo_ver_text", label_tuoNode)
    instance.workspace.add_ui("artist_text", label_artistNode)
    instance.workspace.add_ui("connecting_screen_backbtn", back_button)
    instance.workspace.add_ui("background_connecting_screen", background)

    return "connected-to-game"

def mainMenu(instance, previous_state: int = 1):
    """
    Main menu, you can go to the settings menu or play from here, or exit.
    """
    ## Clear all UI. ##
    instance.clear()

    edgegalaxy_font = instance.fontLoader.load("edgegalaxy")
    basic_font = instance.fontLoader.load("gentium_basic")
    kritidev_font = instance.fontLoader.load("kritidev020")

    default_font = basic_font

    if getSetting("language") == instance.languages_enum.HINDI:
        log("Language is set to Hindi, font being used is set to Kriti Dev 020.")
        default_font = kritidev_font


    ## Get splash texts. ##
    SPLASHES = open(
        getAsset("splash_texts", "path")
    ).readlines()

    skybox = instance.objectLoader.loadObject("skybox")
    skybox.reparentTo(instance.render)
    skybox.set_two_sided(True)
    skybox.set_bin("background", 0)
    skybox.set_depth_write(False)
    skybox.set_compass()
    skybox.setScale(1000)
    skybox.set_light_off(1)
    skybox.set_material_off(1)
    skybox.set_color_off(0)

    def skyboxTask(task):
        skybox.setPos(instance.camera, 0, 0, 0)
        return task.cont

    instance.spawnNewTask("skyboxTask", skyboxTask)


    log("The player is currently on the main menu.")

    ## Networking stuff ##
    addr, port = getSetting("networking", "proxy")[0]["ip"], getSetting("networking", "proxy")[0]["port"]
    def _cmd_ingame():  
        instance.networkClient.connect()

    def _cmd_settings():
        instance.change_state(2)
    
    ## UI stuff. ##

    tuoLogo_tex = instance.loader.loadTexture(getAsset("images", "logo_default"))

    tuoLogo = OnscreenImage(
        image = tuoLogo_tex,
        pos = LVecBase3(-0, 0, 0.5),
        scale = (0, 1, 0)
    )

    tuoLogo.setTransparency(TransparencyAttrib.MAlpha)
    tuoLogo.setScale(0.5)

    play_button = Button(text = instance.translator.translate("ui", "play"),
                                text_scale = 0.1, 
                                pos = (0, 0, 0),
                                command = _cmd_ingame,
                                text_font = default_font,
                                instance = instance
    )

    settings_button = Button(
        text = instance.translator.translate("ui", "settings"),
        text_scale = 0.1,
        pos = (0, 0, -0.34),
        command = _cmd_settings,
        text_font = default_font,
        instance = instance
    )

    exit_button = Button(
        text = instance.translator.translate("ui", "exit"),
        text_scale = 0.1,
        pos = (0, 0, -0.68),
        command = instance.quit,
        text_font = default_font,
        instance = instance
    )

    splash_screen_text = TextNode(name = "splash_screen_text")
    splash_screen_text.setAlign(TextNode.ACenter)
    splash_screen_text.setText(random.choice(SPLASHES))
    splash_screen_text.setFont(edgegalaxy_font)

    spl_scrn_txt_node = instance.render2d.attachNewNode(splash_screen_text)
    spl_scrn_txt_node.setScale(0.08)
    spl_scrn_txt_node.setPos((0.5, 0, 0.5))
    spl_scrn_txt_node.setHpr(LVecBase3(-8.8, 0, -8.8))

    instance.spawnNewTask(
        "mainmenu-splash_screen_pop", splash_screen_pop, (None, instance, spl_scrn_txt_node, clip)
    )

    ## PACK INTO WORKSPACE HIERARCHY ##
    instance.workspace.add_ui("play_btn", play_button)
    instance.workspace.add_ui("splash_text", spl_scrn_txt_node)
    instance.workspace.add_ui("tuoLogo", tuoLogo)
    instance.workspace.add_ui("settingsBtn", settings_button)
    instance.workspace.add_ui("exit_button", exit_button)

    return 'menu-close'

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
    

def settingsPage(instance, previous_state: int = 1):
    """
    The settings page.
    """
    instance.clear()

    basicFont = instance.fontLoader.load("gentium_basic")

    settings = getAllSettings()

    videoFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 1),
        frameSize = (-1, 1, -1, 1)
    )

    accessibilityFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 1),
        frameSize = (-1, 1, -1, 1)
    )

    accessibilityFrame.hide()

    def hideVF():
        if videoFrame.is_hidden():
            videoFrame.show()
            accessibilityFrame.hide()
        else:
            videoFrame.hide()
            accessibilityFrame.show()

    def hideAccessibilityF():
        if accessibilityFrame.is_hidden():
            accessibilityFrame.show()
            videoFrame.hide()
        else:
            accessibilityFrame.hide()
            videoFrame.show()

    videoFrameButton = Button(
        text = "Video Settings",
        pos = (-1, 0, 0.2),
        scale = 0.2,
        command = hideVF,
        instance = instance
    )

    audioSettingsButton = Button(
        text = "Audio Settings",
        pos = (-1, 0, -0.2),
        scale = 0.2,
        instance = instance
    )

    accessibilitySettingsButton = Button(
        text = "Accessibility",
        pos = (-1, 0, -0.6),
        scale = 0.2,
        command = hideAccessibilityF,
        instance = instance
    )

    accountSettingsButton = Button(
        text = "Account Settings",
        pos = (-1, 0, -0.8),
        scale = 0.2,
        command = hideAccessibilityF,
        instance = instance
    )

    videoFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    accessibilityFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    fps_header = DirectLabel(
        text = "Framerate", scale = 0.2, pos = (-0.2, 0, 0.8), text_font = basicFont,
        parent = videoFrame
    )

    msaa_header = DirectLabel(
        text = f"MSAA Level [{int(settings['video']['antialiasing_levels'])}]", scale = 0.2,
        pos = (-0.2, 0, 0.2), text_font = basicFont,
        parent = videoFrame
    )

    def FPS_change():
        instance.clock.setMode(ClockObject.MForced)
        instance.clock.setFrameRate(fps_slider['value'])

        settings['video']['max_framerate'] = int(fps_slider['value'])

        fps_header.setText(f"{int(fps_slider['value'])} FPS")

    def msaa_change():
        settings['video']['antialiasing_levels'] = int(msaa_slider['value'])
        msaa_header.setText(f"MSAA Level [{int(msaa_slider['value'])}]")
        instance.pbrPipeline.msaa_samples = int(msaa_slider['value'])

    def narratorToggle():
        settings['accessibility']['narrator'] = not settings['accessibility']['narrator']

        if settings['accessibility']['narrator']:
            narrator_toggleButton.setText("Narrator: On")
        else:
            narrator_toggleButton.setText("Narrator: Off")

        instance.narrator.refresh()

    def close():
        instance.change_state(previous_state)
        dumpSetting(settings)

    fps_slider = DirectSlider(
        range = (10, 240), value = settings['video']['max_framerate'], pageSize = 3, command = FPS_change,
        scale = 0.5, pos = (-0.2, 0, 0.5),
        parent = videoFrame
    )

    msaa_slider = DirectSlider(
        range = (0, 8), value = settings['video']['antialiasing_levels'], pageSize = 3, command = msaa_change,
        pos = (-0.2, 0, -0.1),
        parent = videoFrame, scale = 0.5
    )

    narrator_toggleButton = Button(
        instance = instance,
        text = "Narrator: ???",
        text_scale = 0.1,
        pos = (-0.2, 0, 0.5),
        text_font = basicFont,
        command = narratorToggle,
        parent = accessibilityFrame
    )

    if settings['accessibility']['narrator']:
        narrator_toggleButton.setText("Narrator: On")
    else:
        narrator_toggleButton.setText("Narrator: Off")

    backBtn = Button(
        instance = instance,
        text = "Back",
        text_scale = 0.1,
        pos = (-0.2, 0, -0.5),
        text_font = basicFont,
        command = close
    )

    instance.workspace.add_ui("narrator_toggle", narrator_toggleButton)
    instance.workspace.add_ui("backBtn", backBtn)
    instance.workspace.add_ui("videoFrame", videoFrame)
    instance.workspace.add_ui("fps_slider", fps_slider)
    instance.workspace.add_ui("fps_header", fps_header)
    instance.workspace.add_ui("videoFrameButton", videoFrameButton)
    instance.workspace.add_ui("audioFrameButton", audioSettingsButton)
    instance.workspace.add_ui("accessibilityFrameButton", accessibilitySettingsButton)
    instance.workspace.add_ui("accountSettingsButton", accountSettingsButton)
    instance.workspace.add_ui("videoFrame", videoFrame)
    instance.workspace.add_ui("msaa_slider", msaa_slider)
    instance.workspace.add_ui("msaa_header", msaa_header)
    instance.workspace.add_ui("accessibilityFrame", accessibilityFrame)

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