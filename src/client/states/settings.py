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
from math import sin, pi

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
        pos = (-1, 0, 0.8),
        scale = 0.2,
        command = hideVF,
        instance = instance
    )

    audioSettingsButton = Button(
        text = "Audio Settings",
        pos = (-1, 0, 0.4),
        scale = 0.2,
        instance = instance
    )

    accessibilitySettingsButton = Button(
        text = "Accessibility",
        pos = (-1, 0, 0),
        scale = 0.2,
        command = hideAccessibilityF,
        instance = instance
    )

    accountSettingsButton = Button(
        text = "Account Settings",
        pos = (-1, 0, -0.4),
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

    def FPS_change():
        instance.clock.setMode(ClockObject.MForced)
        instance.clock.setFrameRate(fps_slider['value'])

        settings['video']['max_framerate'] = int(fps_slider['value'])

        fps_header.setText(f"{int(fps_slider['value'])} FPS")

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
        pos = (-1, 0, -0.8),
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
    instance.workspace.add_ui("accessibilityFrame", accessibilityFrame)