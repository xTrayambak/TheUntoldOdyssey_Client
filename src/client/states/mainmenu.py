import gc
import json
import limeade
import random
import sys
import threading
from datetime import datetime
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.task import Task
from distutils.command.sdist import sdist
from math import sin, pi
from panda3d.core import CardMaker, TextNode, GeoMipTerrain, Texture, TextureStage, DirectionalLight, AmbientLight, \
    ClockObject, LVecBase3, LVecBase4f, TransparencyAttrib, AmbientLight
from time import sleep

from src.client.loader import getAsset, getAllFromCategory
from src.client.objects import Object
from src.client.settingsreader import *
from src.client.shaderutil import loadAllShaders
from src.client.tasks import *
from src.client.ui.button import Button
from src.client.ui.text import Text
from src.client.util.math import *
from src.log import log, warn

FESTIVALS = {
    "18-03": "Happy Holi!",
    "01-04": "Happy Hindu New Year!",
    "02-04": "Eid Mubarak!",
    "06-06": "Happy Birthday Trayambak!",
    "25-12": "Merry Christmas!",
    "18-01": "We all must strive for a free internet, with no monopolies!",
    "01-01": "Happy New Year!"
}

def mainMenu(instance, previous_state: int = 1):
    """
    Main menu, you can go to the settings menu or play from here, or exit.
    """
    limeade.refresh()
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

    skybox = Object(instance, "skybox")
    skybox.reparentTo(instance.render)
    skybox.set_two_sided(True)
    skybox.set_bin("background", 0)
    skybox.set_depth_write(False)
    skybox.set_compass()
    skybox.setScale(5000)
    skybox.set_light_off(1)
    skybox.set_material_off(0)
    skybox.set_color_off(1)

    '''def cameraSpinTask(task):
        if instance.state != instance.states_enum.MENU and instance.state != instance.states_enum.SETTINGS:
            return task.done
        
        instance.camera.setHpr(
            (
                sin(instance.clock.getFrameTime() / 2.5) * 5.9, 
                sin(instance.clock.getFrameTime() / 1.5) * 5,
                instance.clock.getFrameTime() * -1
            ))
        return task.cont'''

    def skyboxTask(task):
        skybox.setPos((0, 0, 0))
        skybox.setHpr(
            LVecBase3(
                instance.clock.getFrameTime() / 8,
                instance.clock.getFrameTime() / 8,
                instance.clock.getFrameTime() / 8
            )
        )
        return task.cont

    instance.spawnNewTask("skyboxTask", skyboxTask)
    #instance.spawnNewTask("cameraSpinTask", cameraSpinTask)


    log("The player is currently on the main menu.")

    ## Networking stuff ##
    addr, port = getSetting("networking", "proxy")[0]["ip"], getSetting("networking", "proxy")[0]["port"]
    def _cmd_ingame():  
        instance.networkClient.connect(addr, port)

    def _cmd_settings():
        instance.change_state(2)
    
    ## UI stuff. ##

    tuoLogo_tex = instance.loader.loadTexture(getAsset("images", "logo_default"))

    """tuoLogo = CardMaker(
        'tuoLogo'
    )

    tuoLogo_card = instance.render.attachNewNode(tuoLogo.generate())
    tuoLogo_card.setPos(LVecBase3(-0, 0, 0.5))
    tuoLogo_card.setScale((1, 1, 1))

    tuoLogo_card.setTexture(tuoLogo_tex)"""

    tuoLogo = OnscreenImage(
        image = tuoLogo_tex,
        pos = LVecBase3(-0, 0, 0.5),
        scale = (0.5, 1, 0.5)
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
    splash_txt = random.choice(SPLASHES)
    time_split = datetime.now().strftime("%d-%m")

    log(f"Simple day/month is {time_split}; checking if a festival is occuring.")

    if time_split in FESTIVALS:
        splash_txt = FESTIVALS[time_split]

    if instance.development_build:
        splash_txt = "This build of the game is a development build, and is not the final product.\nBugs and glitches are to be fixed\nand features may change in the final product."
    elif instance.gamereview_build:
        splash_txt = "This build is for a game reviewer, it is not the final product."

    splash_screen_text = Text(instance, basic_font, splash_txt, 0.09, (0.5, 0, 0.5))
    splash_screen_text.setHpr(LVecBase3(-8.8, 0, -8.8))

    if instance.gamereview_build or instance.development_build:
        def rgb_task(task):
            # nifty comprehension.
            color_rgb_list = [sin((instance.getTimeElapsed() * x) - instance.getDt()) for x in range(3)]
            color_rgb_list.append(1.0)

            splash_screen_text.setColor(
                LVecBase4f(*color_rgb_list)
            )

            return task.cont

        instance.spawnNewTask('rgb_text_task', rgb_task)

    instance.spawnNewTask(
        "mainmenu-splash_screen_pop", splash_screen_pop, (None, instance, splash_screen_text, clip)
    )

    tuo_ver_text = Text(instance, basic_font, "The Untold Odyssey {}".format(instance.version), 0.05, (1.1, 0, -0.9))
    tuo_ver_text.setColor((0, 0, 0))

    syntax_copyright_warning = Text(instance, basic_font, "[W](C) Syntax Studios 2022; do not share!", 0.05, (-1.1, 0, -0.9))
    syntax_copyright_warning.setColor((0, 0, 0))

    ## PACK INTO WORKSPACE HIERARCHY ##
    instance.workspace.add_ui("play_btn", play_button)
    instance.workspace.add_ui("splash_text", splash_screen_text)
    instance.workspace.add_ui("tuoLogo", tuoLogo)
    instance.workspace.add_ui("settingsBtn", settings_button)
    instance.workspace.add_ui("exit_button", exit_button)
    instance.workspace.add_ui("tuo_ver_text", tuo_ver_text)
    instance.workspace.add_ui("syntax_copyright_warning", syntax_copyright_warning)

    return 'menu-close'