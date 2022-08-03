#!/usr/bin/env python3

"""
Managed class for the game's window and running everything, including the workspace, every entity and
networking.

Very good already, doesn't need too much refactoring later.
"""

import gc
import os
import panda3d
import time
from datetime import datetime
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectFrame import DirectFrame
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import ClockObject
from panda3d.core import WindowProperties
from panda3d.core import loadPrcFile

from src.client import shared
from src.client.audioloader import AudioLoader
from src.client.browserutil import BrowserUtil
from src.client.fontloader import FontLoader
from src.client.hardware import HardwareUtil
from src.client.libnarrator import *
from src.client.managers.ambience import AmbienceManager
from src.client.managers.input import InputManager
from src.client.managers.presence import RPCManager
from src.client.maploader import MapLoader
from src.client.narrator_dialog_finder import NarratorDialogFinder
from src.client.networking import NetworkClient
from src.client.objectloader import ObjectLoader
from src.client.player import Player
from src.client.recordingutil import RecordingUtil
from src.client.settingsreader import *
from src.client.shared import *
from src.client.syntaxutil.authlib import Authenticator
from src.client.textureloader import TextureLoader
from src.client.translationutil import TranslationUtility
from src.client.ui.button import *
from src.client.ui.text import *
from src.client.vfxmanager import VFXManager
from src.client.workspace import Workspace
from src.log import log, warn

VERSION = open("VER").read()

PROPERTIES = WindowProperties()
PROPERTIES.setTitle("The Untold Odyssey {} | Main Menu".format(VERSION))

class TUO(ShowBase):
    """
    Initialize the game client.
    """
    def __init__(self, memory_max: int = 800, token: str = ""):
        start_time = time.time()
        log(f"The Untold Odyssey {VERSION} loaded up! Initializing Panda3D.")
        loadPrcFile("assets/config.prc")
        ShowBase.__init__(self)

        self.win.requestProperties(PROPERTIES)

        # TUO Authlib
        self.authenticator = Authenticator(self)

        # GameState
        self.state = GameStates.MENU

        # Workspace for physics and objects
        self.workspace = Workspace()
        self.workspace.init(self)

        # Network client
        self.network_client = NetworkClient(self)

        # Narrator dialog finding utility
        self.narrator_dialog_finder = NarratorDialogFinder(getSetting("language"))

        # Narrator/TTS utility
        self.narrator = NarratorUtil(self)

        # Text translator utility
        self.translator = TranslationUtility(getSetting("language"))

        # Video/screenshot capture utility
        self.recordingUtil = RecordingUtil(self)

        # Hardware specs detection utility
        self.hardware_util = HardwareUtil()
        self.hardware_util.get()

        # Audio loading utility
        self.audioLoader = AudioLoader(self)
        self.rpcManager = None

        # Ambience Manager
        self.ambienceManager = AmbienceManager(self)

        # VFX manager (TUOFX)
        #self.vfxmanager = VFXManager(self)
        #self.vfxmanager.load_file(open('assets/effects/menu_panorama_spin.tuofx'))

        log(f"OpenGL: {self.hardware_util.gl_version} || Vendor: {self.hardware_util.gpu_vendor}", "Worker/Bootstrap")
        
        self.clock = ClockObject()

        log(f"Panda3D lib location: [{panda3d.__file__}]", "Worker/Bootstrap")

        try:
            self.rpc_manager = RPCManager(self)
        except Exception as exc:
            log(f"Failed to initialize Discord rich presence. [{exc}]")

        self.fontLoader = FontLoader(self)
        self.textureLoader = TextureLoader(self)
        self.objectLoader = ObjectLoader(self)
        self.mapLoader = MapLoader(self)
        self.player = Player(self, "player", "playertest_default")
        self.token = token
        self.debug_mode = os.path.exists("DEBUG_MODE")

        self.time_now = datetime.now()

        self.date_info = time_now.strftime("%d-%m-%y")
        self.time_info = time_now.strftime('%H:%M:%S')

        self.globals = {'world_select': -1}

        log(f"Date info: {self.date_info}\nTime info: {self.time_info}", "Worker/TimeDetector")
        log(f"Syntax Studios account token is [{token}]", "Worker/Config")

        self.authenticationServerStatus = self.authenticator.get_auth_server_status()

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
            self.pbrPipeline.enable_shadows = False"""

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

        self.closing = False

        self.inputManager = InputManager(self)
        self.inputManager.init()
        self.inputManager.hook()

        self.development_build = False
        self.gamereview_build = False

        if 'dev' in VERSION:
            self.development_build = True
        elif 'gamereviewer' in VERSION:
            self.gamereview_build = True

        self.paused = False
        self.renderPipeline = None

        self.browser = BrowserUtil()

        self.clock.setMode(ClockObject.MForced)

        log(f"Max framerate is capped to [{self.settings['video']['max_framerate']}] FPS.")
        self.clock.setFrameRate(
            self.settings["video"]["max_framerate"]
        )
        
        self.spawnNewTask("tuo-poll", self.poll)

        self.modules = []

        log("TUO client instance initialized successfully within {} ms".format(time.time() - start_time), "Worker/StartupFinalizer")


    def pause_menu(self):
        if self.state != GameStates.INGAME and self.state != GameStates.DEBUG: return

        if self.paused == False:
            self.paused = True
        else:
            self.paused = False
        
        self._pause_menu(self.paused)


    def add_module(self, module):
        self.modules.append(module(self))


    def is_closing(self) -> bool: 
        """
        Return a `bool` indicating if an exit process is going on.
        """
        return self.closing

    
    def debug_state_secret(self):
        """
        Debug state secret key.
        """ 
        self.change_state(GameStates.END_CREDITS)


    def getDt(self) -> int | float:
        """
        Get the delta time component of the TUO instance.
        """
        return self.clock.getDt()


    def getTimeElapsed(self) -> int | float:
        """
        Get the time elapsed since Panda3D was initialized. This value only increments and is good for sine waves.
        """
        return self.clock.getFrameTime()


    def getFrameTime(self):
        return self.getTimeElapsed()


    def _pause_menu(self, isPaused: bool):
        """
        Show/hide the pause menu based on the `bool` passed.
        """
        if isPaused:
            self.narrator.say("menu.pause.enable")
            self.workspace.getComponent("ui", "paused_text").show()
            self.workspace.getComponent("ui", "return_to_menu_button").show()
            self.workspace.getComponent("ui", "settings_button").show()
        else:
            self.narrator.say("menu.pause.disable")
            self.workspace.getComponent("ui", "settings_button").hide()
            self.workspace.getComponent("ui", "paused_text").hide()
            self.workspace.getComponent("ui", "return_to_menu_button").hide()


    def getSharedData(self):
        return shared


    def setFov(self, value: int):
        self.camLens.setFov(value)


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
        self.networkClient.disconnect()
        self.change_state(1)


    def stop_music(self):
        self.ambienceManager.stop_all_tracks()


    def poll(self, task):
        """
        Poll the in-game clock responsible for some fancy mathematics.

        TUO.poll -> TUO.clock.tick
        """
        self.clock.tick()

        for module in self.modules:
            module.tick(self)

        return Task.cont


    def change_state(self, state: int, extArgs: list = None):
        """
        Change the game's story/part "state"; basically tell the game at which point of gameplay it should switch to.
        Eg. menu, loading screen, in-game or connecting screen.
        """
        self.previousState = self.state
        self.state = GameStates(state)
        self.update(extArgs)

        self.set_title('The Untold Odyssey {} | {}'.format(self.version, GAMESTATES_TO_STRING[self.state]))

        if self.state == GameStates.SETTINGS and self.previousState == GameStates.INGAME:
            return
        elif self.state == GameStates.INGAME and self.previousState == GameStates.SETTINGS:
            return
        elif self.previousState == GameStates.MENU and self.state == GameStates.SETTINGS:
            return
        elif self.previousState == GameStates.SETTINGS and self.state == GameStates.MENU:
            return

        self.stop_music()


    def set_title(self, title: str):
        assert type(title) == str, 'Window title must be string!'
        PROPERTIES = WindowProperties()
        PROPERTIES.setTitle(title)

        self.win.requestProperties(PROPERTIES)


    def new_task(self, name, function, args = None):
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
        

    def spawnNewTask(self, name, function, args = None):
        """
        This is soon to be deprecated as per the refactoring. Use `TUO.new_task` instead.
        """
        return self.new_task(name, function, args)


    def clear(self):
        """
        Clear all UI objects on the screen using NodePath.removeNode
        """
        for name in self.workspace.objects["ui"]:
            obj = self.workspace.objects["ui"][name]

            try:
                obj.removeNode()
            except:
                obj.destroy()
            
        gc.collect()



    def update(self, extArgs: list = None):
        """
        Updates the game state manager.

        TUO.update() -> state_execution[state] <args=self (TUO instance), previousState (GameStates)>
        """
        if not extArgs: GAMESTATE_TO_FUNC[self.state](self, self.previousState)
        else: GAMESTATE_TO_FUNC[self.state](self, self.previousState, *extArgs)


    def getState(self):
        """
        Give the state of the game.

        TUO.getState() -> `src.client.shared.GameStates`
        """
        return GameStates(self.state)



    def getAllStates(self):
        """
        Get a list of all game states, in case you cannot import the shared file because of a circular import.

        TUO.getAllStates() -> `src.client.shared.GameStates`
        """
        return self.states_enum

    
    def initialize_pbr_pipeline(self):
        sys.path.insert(0, "src/client/render_pipeline")
        from src.client.render_pipeline.rpcore.render_pipeline import RenderPipeline
        self.renderPipeline = RenderPipeline()
        #self.renderPipeline.daytime_mgr.time = "11:55"
        self.renderPipeline.pre_showbase_init()
        self.renderPipeline.create(self)


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
        self.new_task(name='ambience_manager_update', function=self.ambienceManager._update)
        self.authenticator.start_auth()
        
        if self.max_mem < 500:
            warn("The game has lesser than 500 MB of memory allocated!")
            self.warn(
                "You have allocated less than 500MB to the game!",
                "The game may crash and you may face lag!\nChange this in the launcher settings if possible.",
                "I understand.",
                "I will restart the game.",
                exitFunc = self.quit
            )
        
        if self.hardware_util.gl_version[0] == 4 and self.hardware_util.gl_version[1] > 2:
            log(f"This GPU does support OpenGL 4.3! [MAJOR={self.hardware_util.gl_version[0]};MINOR={self.hardware_util.gl_version[1]}]", "Worker/Hardware")
            if getSetting("video", "pbr") == True:
                log("Initializing tobspr's render pipeline! May the ricing begin!", "Worker/PBR")
                self.initialize_pbr_pipeline()
        else:
            warn(f"This GPU does not support OpenGL 4.3! [MAJOR={self.hardware_util.gl_version[0]};MINOR={self.hardware_util.gl_version[1]}]")
            settings = getAllSettings()
            settings['video']['pbr'] = False

            dumpSetting(settings)
            self.warn("Your GPU does not support OpenGL 4.3!", "The game will run as usual,\nhowever, features like PBR will\nnot work. If you have a new GPU, try updating\nyour drivers.", "OK.", "HELP!", exitFunc = lambda: self.browser.open(""))


    def quit(self):
        """
        Quit the internal managers, and tell Panda3D to stop the window.

        TUO.quit -> self.closeWindow <args=[win=self.win]>
                    self.finalizeExit
        """
        log("The Untold Odyssey is now stopping!", "Worker/Exit")
        self.ambienceManager.running = False
        self.closing = True
        gc.collect()
        self.closeWindow(win=self.win)
        self.finalizeExit()
