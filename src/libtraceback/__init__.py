import sys
import os
import random


def get_extensions():  return "~~NONE~~: PYGLET NOT INSTALLED."
def get_vendor():  return "~~NONE~~: PYGLET NOT INSTALLED."
def get_version():  return "~~NONE~~: PYGLET NOT INSTALLED."
def get_renderer(): return "~~NONE~~: PYGLET NOT INSTALLED."

from src.log import log, fatal, warn
from src.telemetry import telemetrySend_crash

CRASH_TXTS = [
    "Wait, you hadn't completed the ice bridge?",
    "Ya-hoo hoo hui!",
    "AHHHHHHH!",
    "I'm sorry. :-(",
    "Have you tried turning it on and off?",
    "This is a level-5 problem, tell Unreichvelt.",
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
    "There is a bug among us! Sorry, not sorry for the stupid reference.",
    f"As a sorry for this inconvenience, we have handed you a free muffin ticket. Redeem at your nearest Syntax Store. Claim it before it expires! [{random.randint(-sys.maxsize, sys.maxsize)}]",
    "It isn't a bug, it's an intentional feature, dummy!",
    "Get trolled!!!!!11",
    "Super idol de shiao rong, dou mei ni de tian ba yue jheng ooh de yang guang dou mei ni yao yan re ai yi bai ling ooh du de ni didi ching chun de jheng liu shui!",
    "(╯°□°）╯︵ ┻━┻ I'm mad!!!!",
    "Go listen to some music whilst I'm at it!",
    "Hahaha, game crash go brrrrr..",
    "Haha, this is totally not blatantly stolen from Mojang.",
    "BAHAHAHAHAHA DESERVED!!!1111",
    "UMadeline?",
    "sooo noob, fix that crash yourself -Lucy",
    "Objection! Trayambak, why did this game crash? -Nat",
    "KREEEEEEE -Laz",
    "[insert the wittiest and most hilarious comment to make the player forget the pain they are dealing with]",
    "Cyberpunk 2077 moment, amirite!",
    "If you are a speedrunner and were about to beat the game, I have in-fact, committed a sin. God, please forgive me. -Trayambak",
    "Zamn!!! She took up 5 gigabytes of memory and crashed the game? Zad!!!1",
    "Yo mama so fat that she took up all the memory the game had! Haha, please laugh I am held at gunpoint help nir0wjiwejrkweoiruewrq",
    "You should try listening to the Celeste OST!",
    "You should try listening to The Untold Odyssey's OST!",
    "You should try listening to the Minecraft OST!",
    "Before we diagnose the crash, I'd like to thank our sponsor, amogussusfard VPN.",
    "Don't go full libre mode if you use a NVIDIA GPU, DUMMY! THEY DON'T SUPPORT FREE AS IN FREEDOM!",
    """
    I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.
    Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.
    There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!
    """

]

def get_extensions_string(max_limit: int = 10) -> str:
    """
    Get a neatly formatted string of OpenGL extensions on this really fancy GPU.
    """
    extensions = get_extensions()

    if type(extensions) == str: return extensions

    string = ""
    _extStr = ""

    extensions = list(extensions)

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
        warn(f"Could not dump OpenGL renderer data to /assets/logs/gl_ext.log due to error.\n[{exc}]")

    return string

def log_traceback(instance=None):
    """
    Log all the traceback found into the log so people can send it to us so we can look at it and fix it.
    """
    full_exc = sys.exc_info()

    if instance == None:
        VERSION = "~~INSTANCE NOT INITIALIZED, VERSION NOT FOUND~~"
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

    telemetrySend_crash(log, instance)

    fatal(string)