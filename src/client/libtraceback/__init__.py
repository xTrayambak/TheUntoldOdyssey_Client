import sys
import os
import random

from pyglet.gl.gl_info import *

from src.client.log import log, warn

CRASH_TXTS = [
    "Wait, you hadn't completed the ice bridge?",
    "Ya-hoo hoo hui!",
    "AHHHHHHH!",
    "I'm sorry. :-(",
    "Have you tried turning it on and off?",
    "This is a level-5 problem, tell Night.",
    "The Untold Odyssey is no more! It has ceased to exist!",
    "-99999 social credits for me!",
    "Awwww, too bad it crashed. Now go touch grass.",
    "I told the rendering engine to not have Pineapple Pizza! Well, we're here now.",
    "It crashed? How mediocre!!!",
    "Feed it your RAM!",
    "Download the patch, available in your nearest stores!",
    "Pay us 50$ to fix it!",
    "Your game has been freezed by the grass-toucher squad!",
    "This. Is. Sparta!!!!",
    "/o/ Buggy game dabs!"
]

def get_extensions_string():
    extensions = get_extensions()

    string = ""
    for _ext in extensions:
        string += f"\t{_ext}\n"

def log_traceback(instance):
    full_exc = sys.exc_info()
    
    string = f"""
    The game has crashed, exiting.

    # {random.choice(CRASH_TXTS)}

    Configurations:
    GPU: {get_renderer()}
    Vendor: {get_vendor()}
    OpenGL version: {get_version()}
    OpenGL extensions loaded: {get_extensions_string()}

    The Untold Odyssey Version: {instance.version}
    Python version: {sys.version}

    Platform: {sys.platform}

    Full traceback (sys.exc_info):
    {full_exc[0].__name__}: {full_exc[1]}

    [IF YOUR GAME IS MODDED, CONTACT THE MOD DEVELOPERS FIRST BEFORE CONTACTING US.]
    [The Untold Odyssey, developed by Syntax Studios (2022)]
    """

    warn(string)