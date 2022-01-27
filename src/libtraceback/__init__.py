import sys
import os
import random

try:
    from pyglet.gl.gl_info import *
except ModuleNotFoundError:
    def get_extensions():  return "~~NONE~~: PYGLET NOT INSTALLED."
    def get_vendor():  return "~~NONE~~: PYGLET NOT INSTALLED."
    def get_version():  return "~~NONE~~: PYGLET NOT INSTALLED."
    def get_renderer(): return "~~NONE~~: PYGLET NOT INSTALLED."

from src.log import log, warn

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
    "/o/ Buggy game dabs!",
    "There is a bug among us! Sorry, not sorry.",
    f"As a sorry for this inconvenience, we have handed you a free muffin ticket. Redeem at your nearest Syntax Store. Claim it before it expires! [{random.randint(-sys.maxsize, sys.maxsize)}]",
    "It isn't a bug, it's an intentional feature, dummy!",
    "Get trolled!!!!!11",
    "Super idol de shiao rong dou mei ni de tian Ba yue jheng ooh de yang guang dou mei ni yao yan Re ai yi bai ling ooh du de ni Didi ching chun de jheng liu shui!",
    "(╯°□°）╯︵ ┻━┻ I'm mad!!!!",
    "Go listen to some music whilst I'm at it!",
    "Hahaha, game crash go brrrrr..",
    ""
]

def get_extensions_string(max_limit: int = 9):
    """
    Get a neatly formatted string of OpenGL extensions on this really fancy GPU.
    """
    extensions = get_extensions()

    if type(extensions) == str: return extensions

    string = ""
    _extStr = ""

    for _ext in extensions:
        idx = extensions.index(_ext)
        _extStr += f"{idx} >> {_ext}\n"

        if idx >= max_limit:
            string += f"\tand {len(extensions) - max_limit} more... [DUMPED TO gl_ext.log INSIDE '/assets/logs/']"
            break

        string += f"\t{_ext}\n"

    for _ext in extensions:
        idx = extensions.index(_ext)
        _extStr += f"{idx} >> {_ext}\n"

    try:
        file = open("assets/logs/gl_ext.log", "w")
        file.write("~` The Untold Odyssey `~\n")
        file.write("\tDumped OpenGL data.\n")
        file.write(f":: Loaded OpenGL extensions ::\n{_extStr}")
        file.close()
    except Exception as exc:
        log(f"FATAL >> Could not dump OpenGL renderer data to /assets/logs/gl_ext.log due to error.\n[{exc}]")

    return string

def log_traceback(instance=None):
    """
    Log all the traceback found into the log so people can send it to us so we can look at it and fix it.
    """
    full_exc = sys.exc_info()

    if instance == None:
        VERSION = None
    else:
        VERSION = instance.version
    
    string = f"""
    The game has crashed, exiting.

    # {random.choice(CRASH_TXTS)}

    Configurations:
    GPU: {get_renderer()}
    Vendor: {get_vendor()}
    OpenGL version: {get_version()}
    OpenGL extensions loaded: {get_extensions_string()}

    The Untold Odyssey Version: {VERSION}
    Python version: {sys.version}

    Platform: {sys.platform}

    Full traceback (sys.exc_info):
    {full_exc[0].__name__}: {full_exc[1]}

    [IF YOUR GAME IS MODDED, CONTACT THE MOD DEVELOPERS FIRST BEFORE CONTACTING US.]
    [The Untold Odyssey, developed by Syntax Studios (2022)]
    """

    warn(string)