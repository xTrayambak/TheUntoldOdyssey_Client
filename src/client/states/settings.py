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

from math import sin, pi

STATUS_TO_STR = {
    "OK.": "Online",
    "MAINTENANCE.": "Down for Maintenance",
    "NO.": "Offline; likely crashed."
}

def settingsPage(instance, previous_state: int = 1):
    """
    The settings page.
    """
    instance.clear()

    basicFont = instance.fontLoader.load("gentium_basic")
    settings = getAllSettings()

    videoFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 0.5),
        frameSize = (-1, 1, -1, 1)
    )

    accessibilityFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 0.5),
        frameSize = (-1, 1, -1, 1)
    )

    audioSettingsFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 0.5),
        frameSize = (-1, 1, -1, 1)
    )

    accountSettingsFrame = DirectFrame(
        frameColor = (0.5, 0.5, 0.5, 0.5),
        frameSize = (-1, 1, -1, 1)
    )

    accessibilityFrame.hide()
    accountSettingsFrame.hide()

    def hideVF():
        if videoFrame.is_hidden():
            videoFrame.show()
            accessibilityFrame.hide()
            audioSettingsFrame.hide()
            accountSettingsFrame.hide()
        else:
            videoFrame.hide()

    def hideAccessibilityF():
        if accessibilityFrame.is_hidden():
            accessibilityFrame.show()
            accountSettingsFrame.hide()
            videoFrame.hide()
            audioSettingsFrame.hide()
        else:
            accessibilityFrame.hide()

    def hideAccountF():
        if accountSettingsFrame.is_hidden():
            accountSettingsFrame.show()
            accessibilityFrame.hide()
            audioSettingsFrame.hide()
            videoFrame.hide()
        else:
            accountSettingsFrame.hide()

    def hideAudioF():
        if audioSettingsFrame.is_hidden():
            audioSettingsFrame.show()
            accountSettingsFrame.hide()
            videoFrame.hide()
            accessibilityFrame.hide()
        else:
            audioSettingsFrame.hide()

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
        instance = instance,
        command = hideAudioF
    )

    audioSettingsFrame.hide()

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
        command = hideAccountF,
        instance = instance
    )

    videoFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    accessibilityFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    audioSettingsFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    accountSettingsFrame.setPos(
        LVecBase3(1, 0, -0)
    )

    fps_header = DirectLabel(
        text = "Framerate", scale = 0.2, pos = (-0.2, 0, 0.8), text_font = basicFont,
        parent = videoFrame
    )

    audio_volume_header = DirectLabel(
        text = f"Master ({int(getSetting('volumes', 'master'))}%)", scale = 0.2, pos = (-0.2, 0, 0.8), text_font=basicFont,
        parent = audioSettingsFrame
    )

    if 'status' in instance.authenticationServerStatus:
        if instance.authenticationServerStatus['status'] in STATUS_TO_STR:
            status = STATUS_TO_STR[instance.authenticationServerStatus['status']]
        else:
            status = instance.authenticationServerStatus['status']
    else:
        status = "No response; probably crashed."

    server_auth_status_header = DirectLabel(
        text=f"AUTH SERVER STATUS:\n{status}",
        scale = 0.1, pos=(-0.2, 0, 0.8), parent = accountSettingsFrame
    )

    def FPS_change():
        instance.clock.setMode(ClockObject.MForced)
        instance.clock.setFrameRate(fps_slider['value'])

        settings['video']['max_framerate'] = int(fps_slider['value'])

        fps_header.setText(f"{int(fps_slider['value'])} FPS")

    def volumeMasterChange():
        audio_volume_header.setText(f"Master ({int(audio_volume_slider['value'])}%)")
        instance.sfxManagerList[0].setVolume(
            audio_volume_slider['value']
        )

        settings['volumes']['master'] = int(audio_volume_slider['value'])

    def narratorToggle():
        if instance.narrator.enabled == None:
            warn("Not messing with narrator as it is disabled due to ESPEAK being missing.", "Worker/NarratorToggle")
            return

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

    audio_volume_slider = DirectSlider(
        range = (0, 100), value = getSetting('volumes', 'master'), pageSize = 3, command = volumeMasterChange, scale = 0.5,
        pos = (-0.2, 0, 0.5),
        parent = audioSettingsFrame
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

    if instance.narrator.enabled == None:
        narrator_toggleButton.setText("Narrator: Not Available.")
        
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
    instance.workspace.add_ui("audioFrame", audioSettingsFrame)
    instance.workspace.add_ui("accessibilityFrame", accessibilityFrame)
    instance.workspace.add_ui("server_auth_status_header", server_auth_status_header)
    instance.workspace.add_ui("account_settings_frame", accountSettingsFrame)