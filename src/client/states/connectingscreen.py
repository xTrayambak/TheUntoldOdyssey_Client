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

if sys.platform != 'linux':
    from pyglet.gl import gl_info as gpu_info
else:
    class gpu_info:
        def get_version():
            return "Unable to detect GPU."
            
from math import sin, pi

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