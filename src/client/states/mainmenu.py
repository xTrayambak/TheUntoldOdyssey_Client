import gc
import json
import limeade
import random
import sys
import threading
from datetime import datetime
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.gui.DirectEntry import DirectEntry

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
from src.client.savefileutil import get_all_savefiles
from src.log import log, warn
from src.client.ui.textinput import TextInput
from src.client import helpers
from src.client.utils import load_image_as_plane

FESTIVALS = {
    "06-06": "Happy Birthday Trayambak!",
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

    skybox = Object(instance, "assets/models/skybox1024.egg")
    skybox.reparentTo(instance.render)
    skybox.set_two_sided(True)
    skybox.set_bin("background", 0)
    skybox.set_depth_write(False)
    skybox.set_compass()
    skybox.setScale(5000)
    skybox.set_light_off(1)
    skybox.set_material_off(0)
    skybox.set_color_off(1)

    def camera_spin_task(task):
        if instance.state != instance.states_enum.MENU and instance.state != instance.states_enum.SETTINGS:
            return task.done
        
        instance.camera.setHpr(
            (
                sin(instance.clock.getFrameTime() / 2.5) * 5.9, 
                sin(instance.clock.getFrameTime() / 1.5) * 5,
                instance.clock.getFrameTime() * -1
            ))
        return task.cont

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

    instance.new_task("skyboxTask", skyboxTask, False)
    #instance.spawnNewTask("cameraSpinTask", cameraSpinTask)


    log("The player is currently on the main menu.")

    ## Networking stuff ##
    addr, port = getSetting("networking", "proxy")[0]["ip"], getSetting("networking", "proxy")[0]["port"]

    def button_singleplayer():
        instance.change_state(3)
        return
        instance.globals['world_select'] = 0

        instance.workspace.get_component('ui', 'status_text').node().setText('')

        savefiles = get_all_savefiles()
        if len(savefiles) > 0:
            log('Found worlds, opening world list instead of world creation screen.')
            helpers.mainmenu_worldlist(instance, savefiles)
            return

        log('Found 0 worlds, opening world creation screen instead of world list.')

        def name_chosen(name: str):
            helpers.mainmenu_worldcreate_screen_001(name, instance)

        save_name = TextInput(instance, name_chosen, '', 'World Name')
        instance.workspace.add_ui('world_name_input', save_name)

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
    
    hammer_ico_64px = load_image_as_plane(instance, 'assets/img/hammer_64px.png', 256)
    hammer_ico_64px.setTransparency(TransparencyAttrib.MAlpha)

    mods_menu_btn = Button(instance,
            text = instance.translator.translate('ui', 'mods'),
            scale = 0.1, 
            pos = (-0.5, 0.5, 0),
            command = lambda: instance.change_state(7)
    )

    play_button = Button(text = instance.translator.translate("ui", "singleplayer"),
                                text_scale = 0.1, 
                                pos = (0, 0, 0),
                                command = button_singleplayer,
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
        splash_txt = "[RGB]This build of the game is a development build, and is not the final product.\nBugs and glitches are to be fixed\nand features may change in the final product."
    elif instance.gamereview_build:
        splash_txt = "[I]This build is for a game reviewer, it is not the final product."

    if splash_txt != "This splash text will never show up in the game, isn't that pretty weird?":
        splash_screen_text = Text(instance, basic_font, splash_txt, 0.09, (0.5, 0, 0.5))
        splash_screen_text.setHpr(LVecBase3(-8.8, 0, -8.8))
    else:
        splash_screen_text = None

    instance.new_task(
        "mainmenu-splash_screen_pop", splash_screen_pop, False, (None, instance, splash_screen_text, clip)
    )

    tuo_ver_text = Text(instance, basic_font, "The Untold Odyssey {}".format(instance.version), 0.05, (1.1, 0, -0.9))
    tuo_ver_text.setColor((0, 0, 0))

    syntax_copyright_warning = Text(instance, basic_font, "[I](C) Syntax Studios 2022; do not share!", 0.05, (-1.1, 0, -0.9))
    syntax_copyright_warning.setColor((0, 0, 0))

    ## PACK INTO WORKSPACE HIERARCHY ##
    instance.workspace.add_ui("play_btn", play_button)
    if splash_screen_text:
        instance.workspace.add_ui("splash_text", splash_screen_text)
    instance.workspace.add_ui("tuoLogo", tuoLogo)
    instance.workspace.add_ui("settingsBtn", settings_button)
    instance.workspace.add_ui("exit_button", exit_button)
    instance.workspace.add_ui("tuo_ver_text", tuo_ver_text)
    instance.workspace.add_ui("syntax_copyright_warning", syntax_copyright_warning)
    instance.workspace.add_ui("mods_btn", mods_menu_btn)
    instance.spawnNewTask('menu_spin_task', camera_spin_task)

    return 'menu-close'
