#!/usr/bin/env python3

"""
Managed class for the game's window and running everything, including the workspace, every entity and
networking.

Very good already, doesn't need too much refactoring later. Proud of this.
"""

import panda3d
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectFrame import DirectFrame
from direct.task import Task
from panda3d.core import loadPrcFile
from panda3d.core import WindowProperties
from panda3d.core import ClockObject
from multiprocessing.pool import ThreadPool

from src.log import log, warn
from src.client.shared import *
from src.client.workspace import Workspace
from src.client.managers.ambience import AmbienceManager
from src.client.managers.input import InputManager
from src.client.networking import NetworkClient
from src.client.managers.presence import RPCManager
from src.client.fontloader import FontLoader
from src.client.textureloader import TextureLoader
from src.client.objectloader import ObjectLoader
from src.client.syntaxutil import SyntaxUtil
from src.client.player import Player
from src.client.translationutil import TranslationUtility
from src.client.maploader import MapLoader
from src.client.libnarrator import *
from src.client.settingsreader import *
from src.client.recordingutil import RecordingUtil
from src.client.syntaxutil.authlib import Authenticator

from src.client.ui.text import *
from src.client.ui.button import *

import gc
import threading
import os
import pathlib

VERSION = open("VER").read()

PROPERTIES = WindowProperties()
PROPERTIES.setTitle("The Untold Odyssey {} | Main Menu".format(VERSION))

class TUO(ShowBase):
    def __init__(self, memory_max: int = 800, token: str = ""):
        log(f"The Untold Odyssey {VERSION} loaded up!")
        log("Initializing Panda3D rendering engine.")
        loadPrcFile("assets/config.prc")
        ShowBase.__init__(self)
        log("Panda3D initialized.")

        self.win.requestProperties(PROPERTIES)

        ### START DEFINING VARIABLES ###
        self.authenticator = Authenticator(self)
        self.state = GameStates.MENU
        self.workspace = Workspace()
        self.workspace.init(self)
        self.ambienceManager = AmbienceManager()
        self.networkClient = NetworkClient(self)
        self.narrator = NarratorUtil()
        self.translator = TranslationUtility(
            getSetting("language")
        )
        self.recordingUtil = RecordingUtil(self)
        self.rpcManager = None
        
        self.clock = ClockObject()

        log(f"Panda3D lib location: [{panda3d.__file__}]")

        try:
            self.rpcManager = RPCManager(self)
        except Exception as exc:
            log(f"Failed to initialize Discord rich presence. [{exc}]")

        self.fontLoader = FontLoader(self)
        self.textureLoader = TextureLoader(self)
        self.objectLoader = ObjectLoader(self)
        self.syntaxUtil = SyntaxUtil(self)
        self.mapLoader = MapLoader(self)
        self.player = Player(self, "player", "playertest_default")
        self.token = token

        #self.disableMouse()

        self.sfxManagerList[0].setVolume(
            getSetting("volumes", "master")
        )

        #self.commonFilters = CommonFilters(self.win, self.cam)
        #self.commonFilters.setAmbientOcclusion(16, 0.05, 2, 0.01, 0.0000002)

        """self.pbrPipeline = simplepbr.init(
            msaa_samples = getSetting("video", "antialiasing_levels"),
            enable_shadows = True,
            enable_fog = True,
            use_occlusion_maps = True
        )

        if not self.pbrPipeline.use_330:
            warn("The GPU is NOT capable of running OpenGL 3.30; shadows will not be enabled by SimplePBR.")
            self.pbrPipeline.enable_shadows = Falsel"""

        self.states_enum = GameStates
        self.languages_enum = Language
        self.max_mem = int(memory_max)

        self.inGameTime = 0.0
        self.previousState = GameStates.MENU

        self.game = None

        self.version = VERSION
        self.wireframeIsOn = False
        self.fpsCounterIsOn = False
        self.settings = getAllSettings()

        self.inputManager = InputManager(self)
        self.inputManager.init()
        self.inputManager.hook()

        self.paused = False

        self.clock.setMode(ClockObject.MForced)

        log(f"Max framerate is capped to [{self.settings['video']['max_framerate']}] FPS.")
        self.clock.setFrameRate(
            self.settings["video"]["max_framerate"]
        )

        self.syntaxUtil.hook()
        self.spawnNewTask("tuo-poll", self.poll)

        log(f"Maximum memory is set to {self.max_mem} MB")

    def pause_menu(self):
        if self.state != GameStates.INGAME: return

        if self.paused == False:
            self.paused = True
        else:
            self.paused = False
        
        self._pause_menu(self.paused)

    def _pause_menu(self, isPaused: bool):
        if isPaused:
            self.narrator.say("open pause menu")
            self.workspace.getComponent("ui", "paused_text").show()
            self.workspace.getComponent("ui", "return_to_menu_button").show()
            self.workspace.getComponent("ui", "settings_button").show()
        else:
            self.narrator.say("close pause menu")
            self.workspace.getComponent("ui", "settings_button").hide()
            self.workspace.getComponent("ui", "paused_text").hide()
            self.workspace.getComponent("ui", "return_to_menu_button").hide()

    def warn(self, title: str="Lorem Ipsum", description: str="Door Sit", button_confirm_txt: str = "OK", button_exit_txt: str = "NO", confirmFunc=None, exitFunc = None) -> bool:
        """
        Shows a warning onto the screen.

        ======================

                TITLE

            DESCRIPTION

        OPTION1        OPTION2

        ======================
        """
        font = self.fontLoader.load("gentium_basic")

        frame = DirectFrame(parent = self.aspect2d, frameSize=(-2, 2, -2, 2), frameColor=(0.5, 0.5, 0.5, 0.2))
        warning_title = Text(self, font, title, 0.1, (0, 0, 0.5))
        warning_description = Text(self, font, description, 0.1, (0, 0, 0))

        def close_func():
            log("Warning was closed. Result was MENU_DECLINE")
            warning_title.destroy()
            warning_description.destroy()
            confirm_button.destroy()
            exit_button.destroy()
            frame.destroy()
            
            if exitFunc is not None:
                exitFunc()

            return False

        def _confirmfunc():
            log("Warning was closed. Result was MENU_ACCEPT")
            warning_title.destroy()
            warning_description.destroy()
            confirm_button.destroy()
            exit_button.destroy()
            frame.destroy()

            if confirmFunc is not None:
                confirmFunc()
            
            return True

        confirm_button = Button(
            self, button_confirm_txt, 0.1, 0.1, (-0.5, 0, -0.5),
            command = _confirmfunc, text_font = font
        )

        exit_button = Button(
            self, button_exit_txt, 0.1, 0.1, (0.5, 0, -0.5),
            command = close_func, text_font = font
        )

        self.workspace.add_ui("warning_title", warning_title)
        self.workspace.add_ui("warning_description", warning_description)
        self.workspace.add_ui("warning_confirm", confirm_button)
        self.workspace.add_ui("warning_exit", exit_button)

    def quit_to_menu(self):
        self.change_state(1)

    def stop_music(self):
        self.ambienceManager.stop_all_tracks()

    def poll(self, task):
        """
        Poll the in-game clock responsible for some fancy mathematics.

        TUO.poll -> TUO.clock.tick
        """
        self.clock.tick()


        return Task.cont

    def change_state(self, state: int):
        """
        Change the game's story/part "state"; basically tell the game at which point of gameplay it should switch to.
        Eg. menu, loading screen, in-game or connecting screen.

        This is controlled by an Enum, feel free to change it anytime as nothing too technical changes with it.
        Why am I writing docs? Oh wait, yeah, this will probably be open source so 7 year old script kiddies don't accuse
        me of integrating trackers or a Bitcoin miner into the game.
        """
        self.previousState = self.state
        self.state = GameStates(state)
        self.update()

        PROPERTIES = WindowProperties()
        PROPERTIES.setTitle("The Untold Odyssey {} | {}".format(VERSION, GAMESTATES_TO_STRING[self.state]))

        self.win.requestProperties(PROPERTIES)

        if self.state == GameStates.SETTINGS and self.previousState == GameStates.INGAME:
            return
        elif self.state == GameStates.INGAME and self.previousState == GameStates.SETTINGS:
            return
        elif self.previousState == GameStates.MENU and self.state == GameStates.SETTINGS:
            return
        elif self.previousState == GameStates.SETTINGS and self.state == GameStates.MENU:
            return

        self.stop_music()

    def spawnNewTask(self, name, function, args = None):
        """
        Create a new coroutine/task with the name `name` and task/function `function`.
        This function will be called every frame by Panda3D, TUO has no control over it's calling rate once it's hooked.

        !! WARNING !!

        The Task system is a single-threaded cycle-process! Do not call time.sleep or any other thread-pausing function on it!
        It will cause the entire Panda3D rendering system to freeze entirely!
        Instead, in order to block the task/coroutine, call Task.pause inside the task function!

        :: ARGS

        `name` :: The name of the function; required by Panda3D.\n
        `function` :: The function to be converted to a task/coroutine and called by Panda3D.
        """
        return self.taskMgr.add(function, name, extraArgs=args)

    def clear(self):
        """
        Clear all UI objects on the screen using NodePath.removeNode
        """
        for name in self.workspace.objects["ui"]:
            log(f"Removing UI object '{name}'", "Worker/UIClear")
            obj = self.workspace.objects["ui"][name]

            try:
                obj.removeNode()
            except:
                obj.destroy()
            
        gc.collect()

    def update(self):
        """
        Updates the game state manager.

        TUO.update() -> state_execution[state] <args=self (TUO instance), previousState (GameStates)>
        """
        GAMESTATE_TO_FUNC[self.state](self, self.previousState)

    def start_internal_game(self):
        """
        Start the internal game.

        TUO.start_internal_game -> self.update
                                -> self.ambienceManager.update <args=[self]>
                                -> self.rpcManager.run
        """
        if self.rpcManager != None:
            self.rpcManager.run()
            
        self.update()
        self.ambienceManager.update(self)
        self.authenticator.start_auth()
        
        if self.max_mem < 500:
            warn("The game has lesser than 500 MB of memory allocated!")
            self.warn(
                "You have allocated less than 500MB to the game!",
                "The game may crash and you may face lag!",
                "I understand.",
                "Okay."
            )

    def quit(self):
        """
        Quit the internal managers, and tell Panda3D to stop the window.

        TUO.quit -> self.closeWindow <args=[win=self.win]>
                    self.finalizeExit
        """
        self.ambienceManager.running = False
        self.closeWindow(win=self.win)
        self.finalizeExit()