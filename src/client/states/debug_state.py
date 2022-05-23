from time import sleep

from direct.gui.DirectGui import *
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectFrame import DirectFrame
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectOptionMenu import DirectOptionMenu

import psutil
import gc

from panda3d.core import (
    NodePath, TextNode
)

from src.client.loader import getAsset, getAllFromCategory
from src.log import log, warn
from src.client.shaderutil import loadAllShaders
from src.client.settingsreader import *
from src.client.objects import Object
from src.client.tasks import *
from src.client.visual_shared import *

from src.client.ui.button import Button
from src.client.ui.text import Text

import limeade
from math import sin, pi

process = psutil.Process()

def debug_state(instance, previous_state: int = 1):
    limeade.refresh()
    instance.clear()
    instance.setFov(getSetting("video", "fov"))
    """
    Apply visual shaders
    using Panda3D's built-in shader pipeline.
    """
    font = instance.fontLoader.load("gentium_basic")

    debug_frame_info = DirectFrame()

    tuo_version = Text(instance, font, text=f"Debug Mode", scale=0.05, alignment=TextNode.ALeft, position=(-1, 0, 0.8), parent=debug_frame_info)

    
    def settingsPage():
        instance.change_state(2)

    def quit_to_menu():
        instance.quit_to_menu()
        instance.networkClient.last_packet_ms = 0

    paused_text = Text(instance, font, "Game Paused [DEBUG MODE]", 0.09, position = (0, 0, 0.5))

    settings_button = Button(instance, "Settings", 0.1, 0.085, pos=(0, 0, -0.38), text_font=font, command=settingsPage)
    return_to_menu_button = Button(instance, "Quit to Menu", 0.1, 0.085, pos=(0, 0, 0), text_font=font, command=quit_to_menu)

    paused_text.hide()
    return_to_menu_button.hide()
    settings_button.hide()

    test_text_fx_shake = Text(instance, font, "[S]This text is shaaaaking!", 0.1)
    test_text_fx_italic = Text(instance, font, "[I]This text is italic!", 0.1, (0, 0.5, 0))
    test_text_fx_jumble = Text(instance, font, "[J]", 0.1, (0, 1, 0))
    test_text_fx_jumble_text = Text(instance, font, "<- This text is jumbling!", 0.1, (0.5, 1, 0))
    

    instance.workspace.add_ui("paused_text", paused_text)
    instance.workspace.add_ui("return_to_menu_button", return_to_menu_button)
    instance.workspace.add_ui("settings_button", settings_button)
    instance.workspace.add_ui("debug_stats_version", tuo_version)
    instance.workspace.add_ui("text_fx_shake", test_text_fx_shake)
    instance.workspace.add_ui("text_fx_italic", test_text_fx_italic)
    instance.workspace.add_ui("text_fx_jumble", test_text_fx_jumble)
    instance.workspace.add_ui("text_fx_jumble_text", test_text_fx_jumble_text)