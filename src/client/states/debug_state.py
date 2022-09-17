import gc
import limeade
import psutil
import panda3d
import sys
import cpuinfo
import platform

from DirectGuiExtension.DirectOptionMenu import DirectOptionMenu
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import *
from direct.gui.DirectSlider import DirectSlider
from math import sin, pi
from panda3d.core import (
    NodePath, TextNode
)
from time import sleep

from src.client.loader import getAsset, getAllFromCategory
from src.client.objects import Object
from src.client.settingsreader import *
from src.client.shaderutil import loadAllShaders
from src.client.tasks import *
from src.client.ui.button import Button
from src.client.ui.text import Text
from src.client.visual_shared import *
from src.client.hardware.displayutil import DisplayServer
from src.log import log, warn

process = psutil.Process()

DSP_SRV_TO_STR = {
    DisplayServer.WAYLAND: 'Wayland',
    DisplayServer.XORG: 'X11'
}

def debug_state(instance, previous_state: int = 1):
    if not instance.debug_mode: exit(-1)
    limeade.refresh()
    instance.clear()

    font = instance.fontLoader.load("gentium_basic")
    debug_frame_info = DirectFrame()

    tuo_version = Text(instance, font, text=f"TUO {instance.version} [DEBUGGER]", scale=0.1, alignment=TextNode.ALeft, position=(-1, 0, 0.8), parent=debug_frame_info)
    p3d_ver_text = Text(instance, font, text = f'Python {sys.version}\nPanda3D {panda3d.__version__}', scale = 0.1, position = (-1, 0, 0.6), alignment = TextNode.ALeft, parent = debug_frame_info)

    if instance.mod_loader != None:
        modloader_info = Text(instance, font, text = f'Mods: L: {len(instance.mod_loader.mods)}', scale = 0.1, position = (-1, 0, 0.3), alignment = TextNode.ALeft, parent = debug_frame_info)
    else:
        modloader_info = Text(instance, font, text = f'[I]Modding API explicitly disabled.', scale = 0.1, position = (-1, 0, 0.3), alignment = TextNode.ALeft, parent = debug_frame_info)

    hardware_info_str = '''
OpenGL: {}
Vendor: {}
Refresh Rate: {} Hz
'''.format(instance.hardware_util.gl_version_string_detailed, instance.hardware_util.gpu_vendor, instance.hardware_util.display_util.refresh_rate)

    if instance.hardware_util.platform_util.get('os.global.architecture')[0] == 'linux': # sys.platform? What is that? Never heard of it.
        distro_data = instance.hardware_util.platform_util.get('os.linux.distro_data')
        cpu_data = cpuinfo.get_cpu_info()

        hardware_info_str += f'Display Server: {DSP_SRV_TO_STR[instance.hardware_util.display_util.get_display_server()]}\n\n'
        hardware_info_str += f'Distro: {distro_data["name"]}\nBased On: {distro_data["based_on"]}\n\n'
    hardware_info_str += f'CPU: {platform.processor()}\nBITS: {cpu_data["bits"]}\nARCH: {cpu_data["arch"]}\nFREQ: {cpu_data["hz_actual_friendly"]} GHz'

    hardware_info = Text(instance, font, text = hardware_info_str, scale = 0.1, position = (-1, 0, 0.2), alignment = TextNode.ALeft, parent = debug_frame_info)

    def settingsPage():
        instance.change_state(2)

    def quit_to_menu():
        instance.quit_to_menu()

    paused_text = Text(instance, font, "Game Paused [DEBUG MODE]", 0.09, position = (0, 0, 0.5))

    settings_button = Button(instance, "Settings", 0.1, 0.085, pos=(0, 0, -0.38), text_font=font, command=settingsPage)
    return_to_menu_button = Button(instance, "Quit to Menu", 0.1, 0.085, pos=(0, 0, 0), text_font=font, command=quit_to_menu)

    paused_text.hide()
    return_to_menu_button.hide()
    settings_button.hide()

    instance.workspace.add_ui("paused_text", paused_text)
    instance.workspace.add_ui("return_to_menu_button", return_to_menu_button)
    instance.workspace.add_ui("settings_button", settings_button)
    instance.workspace.add_ui("debug_stats_version", tuo_version)
    instance.workspace.add_ui('p3d_ver_text', p3d_ver_text)
    instance.workspace.add_ui('modloader_info', modloader_info)
    instance.workspace.add_ui('hardware_info', hardware_info)
