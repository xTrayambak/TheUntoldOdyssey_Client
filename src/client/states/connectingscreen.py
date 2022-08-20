import gc
import json
import limeade
import random
import sys
import threading
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
from src.log import log, warn


def connectingPage(instance, previous_state: int = 1):
    """
    The "connecting to servers, please wait" page.

    (Arima your art is amazing xddddd)
    """
    limeade.refresh()
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

    label_connecting = TextNode(name = "node_text_connect")

    if instance.globals['world_select'] == 1:
        label_connecting.setText(f"Connecting to [{instance.network_client.connectingTo}]; locating host and establishing connection.")
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
    label_gpu.setText("OpenGL " +instance.hardware_util.gl_version_string_detailed)
    label_gpu.setTextColor((0,0,0,1))
    label_gpu.setAlign(TextNode.ALeft)
    label_gpu.setFont(mangabey_font)
    label_gpuNode = instance.aspect2d.attachNewNode(label_gpu)
    label_gpuNode.setScale(0.07)

    if sys.platform == 'linux':
        import distro
        label_distroData = TextNode(name = "node_linuxdistro")
        label_distroData.setText("{} '{}' Build {} ({} Linux)".format(distro.name(True), distro.codename(), distro.build_number(), distro.like().upper()))
        label_distroData.setTextColor((0, 0, 0, 1))
        label_distroData.setAlign(TextNode.ARight)
        label_distroData.setFont(mangabey_font)
        label_distroNode = instance.aspect2d.attachNewNode(label_distroData)
        label_distroNode.setScale(0.07)

        instance.workspace.add_ui("distroData", label_distroNode)

    label_gpuNode.setPos((-1.9, 0, -0.8))
    label_tuoNode.setPos((-1.9, 0, -0.9))
    label_artistNode.setPos((1.9, 0, -0.9))
    label_distroNode.setPos((1.9, 0, 0.9))

    instance.workspace.add_ui("status_text", label_connectingNode)
    instance.workspace.add_ui("gpu_text", label_gpuNode)
    instance.workspace.add_ui("tuo_ver_text", label_tuoNode)
    instance.workspace.add_ui("artist_text", label_artistNode)
    instance.workspace.add_ui("connecting_screen_backbtn", back_button)
    instance.workspace.add_ui("background_connecting_screen", background)
