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
from src.client.util.math import *

from src.client.ui.button import Button
from src.client.ui.text import Text

from pyglet.gl import gl_info as gpu_info
from math import sin, pi

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
    skybox.setScale(5000)
    skybox.set_light_off(1)
    skybox.set_material_off(0)
    skybox.set_color_off(1)

    def cameraSpinTask(task):
        if instance.state != instance.states_enum.MENU and instance.state != instance.states_enum.SETTINGS:
            return task.done
        
        instance.camera.setHpr(
            (
                sin(instance.clock.getFrameTime() / 2.5) * 5.9, 
                sin(instance.clock.getFrameTime() / 1.5) * 5,
                instance.clock.getFrameTime() * -1
            )
        )
        return task.cont

    def skyboxTask(task):
        skybox.setPos(instance.camera, 0, 0, 0)
        return task.cont

    instance.spawnNewTask("skyboxTask", skyboxTask)
    instance.spawnNewTask("cameraSpinTask", cameraSpinTask)


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
        scale = (1, 1, 1)
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