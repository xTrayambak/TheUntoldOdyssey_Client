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
from panda3d.core import ClockObject, loadPrcFile, WindowProperties, AntialiasAttrib

from src.client import shared
from src.log import log, warn
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
from src.client.modloader import ModLoader
from src.client.vfxmanager import VFXManager
from src.client.workspace import Workspace
from src.client.game import Game
from src.client.event import Event
from src.client.imageloader import ImageLoader
from src.client.camera import Camera

VERSION = open("VER").read()

PROPERTIES = WindowProperties()
PROPERTIES.setTitle("The Untold Odyssey {} | Main Menu".format(VERSION))

class TUO(ShowBase):
    """
    Initialize the game client.
    """
    def __init__(self, memory_max: int = 800, token: str = "", disable_mod_lvm: int = 0):
        start_time = time.time()
        log(f"The Untold Odyssey {VERSION} loaded up! Initializing Panda3D.")
        loadPrcFile("assets/config.prc")
        ShowBase.__init__(self)

        self.win.requestProperties(PROPERTIES)

        # TUO Authlib
        self.authenticator = Authenticator(self)

        # Override camera
        #print(self.camera.getParent()); exit()
        camera = Camera(self)
        self.camera = camera

        # GameState
        self.state = GameStates.MENU

        # Workspace for physics and objects
        self.workspace = Workspace()
        self.workspace.init(self)

        # Network client
        self.network_client = NetworkClient(self)

        # Narrator dialog finding utility
        self.narrator_dialog_finder = NarratorDialogFinder(get_setting("language"))

        # Narrator/TTS utility
        self.narrator = NarratorUtil(self)

        # Text translator utility
        self.translator = TranslationUtility(get_setting("language"))

        # Video/screenshot capture utility
        self.recordingUtil = RecordingUtil(self)

        # Hardware specs detection utility
        self.hardware_util = HardwareUtil()
        self.hardware_util.get()
        
        # This is what LUA scripts get redirected to when they try to access a forbidden object
        self.null_lvm = None

        # Internal clock for fancy math
        self.clock = ClockObject()

        try:
            self.rpc_manager = RPCManager(self)
        except Exception as exc:
            log(f"Failed to initialize Discord rich presence. [{exc}]")
            self.rpc_manager = None

        self.fontLoader = FontLoader(self)
        self.texture_loader = TextureLoader(self)
        self.objectLoader = ObjectLoader(self)
        self.image_loader = ImageLoader(self)
        self.audio_loader = AudioLoader(self)

        self.player = Player(self, "player", "assets/models/monke.egg", [0, 0, 0])
        self.token = token

        self.events = []
        self.modules = []
        self.globals = {
            'world_select': -1,
            'wireframe_is_on': False,
            'fps_counter_is_on': False,
            'time_now': datetime.now(),
            'debug_mode': os.path.exists('DEBUG_MODE')
        }

        self.time_now = datetime.now()

        self.date_info = time_now.strftime("%d-%m-%y")
        self.time_info = time_now.strftime('%H:%M:%S')

        log(f"Date info: {self.date_info}\nTime info: {self.time_info}", "Worker/TimeDetector")
        log(f"Syntax Studios account token is [{token}]", "Worker/Config")

        self.authenticationServerStatus = self.authenticator.get_auth_server_status()

        self.set_volume_master(
            get_setting("volumes", "master")
        )

        self.states_enum = GameStates
        self.languages_enum = Language
        self.max_mem = int(memory_max)

        self.previousState = GameStates.MENU

        self.version = VERSION

        # TODO: Add this to TUO.globals instead.
        self.wireframe_is_on = False
        self.fps_counter_is_on = False

        self.settings = get_all_settings()

        self.closing = False

        self.inputManager = InputManager(self)
        self.inputManager.init()
        self.inputManager.hook()

        self.render.setAntialias(AntialiasAttrib.MAuto)

        self.development_build = False
        self.gamereview_build = False

        if 'dev' in VERSION:
            self.development_build = True
        elif 'gamereviewer' in VERSION:
            self.gamereview_build = True

        self.paused = False
        self.renderPipeline = None
        self.disable_mod_lvm = disable_mod_lvm


        self.browser = BrowserUtil()

        self.clock.setMode(ClockObject.MLimited)
        self.clock.setFrameRate(
            self.settings["video"]["max_framerate"]
        )

        self.new_task("tuo-poll", self.poll)

        log("TUO client instance initialized successfully within {} ms".format(time.time() - start_time), "Worker/StartupFinalizer")
 

    def log(self, msg: str, sender: str = None):
        """
        Logging function for LUA scripts.
        """
        return log(msg, sender)

    def warn(self, msg: str, sender: str = None):
        """
        Warn function for LUA scripts.
        """
        return warn(msg, sender)

    def set_volume_master(self, value: float | int):
        """
        Set the master volume to something.
        """
        self.sfxManagerList[0].setVolume(value)

    def get_volume_master(self) -> float | int:
        """
        Get the master volume.
        """
        return self.sfxManagerList[0].get_volume()

    def toggle_wireframe(self):
        """
        Toggle the wireframe rendering option.
        """
        self.globals['wireframe_on'] = not self.globals['wireframe_is_on']

        if self.globals['wireframe_on']:
            self.wireframe_on()
        else:
            self.wireframe_off()


    def toggle_fps_counter(self):
        """
        Toggle the Panda3D built-in FPS counter.
        """
        self.globals['fps_counter_is_on'] = not self.globals['fps_counter_is_on']
        self.setFrameRateMeter(self.globals['fps_counter_is_on'])


    def pause_menu(self):
        """
        Go to the pause menu.
        """
        if self.state != GameStates.INGAME and self.state != GameStates.DEBUG: return

        if self.paused == False:
            self.paused = True
        else:
            self.paused = False

        self._pause_menu(self.paused)


    def add_module(self, module):
        """
        Add a module (oversimplified DIRECT task) to the execution task.
        """
        self.modules.append(module)
        self.new_task(module.name, module.call_task, (self,))


    def create_event(self, name: str) -> Event:
        """
        Create a new event with the name `name`.
        """
        event = Event(name)
        self.events.append(event)

        return event


    def get_event(self, name: str) -> Event:
        """
        Get an event with the name `name`.
        If no event with said name is found, then None is returned.
        """
        for event in self.events:
            if event.name == name: return event


    def is_closing(self) -> bool:
        """
        Return a `bool` indicating if an exit process is going on.
        """
        return self.closing


    def debug_state_secret(self):
        """
        Debug state secret key.
        """
        self.change_state(GameStates.DEBUG)


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


    def _pause_menu(self, is_paused: bool):
        """
        Show/hide the pause menu based on the `bool` passed.
        """
        if is_paused:
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
        """
        Get all the shared data from src.client.shared
        """
        return shared


    def set_fov(self, value: int):
        """
        Set the FOV.
        """
        self.camLens.setFov(value)


    def get_task_signals(self) -> dict:
        """
        This is meant for the LUA modding API.
        Please refain from using this in the Python codebase, use `direct.task.Task` instead.
        """
        return {'cont': Task.cont, 'done': Task.done, 'pause': Task.pause}


    def warn(self, title: str = "Lorem Ipsum", description: str = "Door Sit", 
             button_confirm_txt: str = "OK", button_exit_txt: str = "NO", 
             confirmFunc = None, exitFunc = None) -> bool:
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
        """
        Quit to the menu screen.
        """
        self.change_state(1)


    def stop_music(self):
        """
        Stop all the music that is currently playing.
        """
        self.audio_loader.stop_all_sounds()


    def poll(self, task):
        """
        Poll the in-game clock responsible for some fancy mathematics.

        TUO.poll -> TUO.clock.tick
        """
        self.clock.tick()

        return Task.cont


    def change_state(self, state: int, extArgs: list = None):
        """
        Change the game's story/part "state"; basically tell the game at which point of gameplay it should switch to.
        Eg. menu, loading screen, in-game or connecting screen.
        """
        self.previous_state = self.state

        # TODO: Deprecate this sometime as this is a violation of PEP-8. Keeping this here for backwards compatibility.
        self.previousState = self.previous_state

        self.state = GameStates(state)
        self.update(extArgs)

        self.get_event('on_state_change').fire([self.state, self.previousState])

        self.set_title('The Untold Odyssey {} | {}'.format(self.version, GAMESTATES_TO_STRING[self.state]))

        if self.state == GameStates.SETTINGS and self.previous_state == GameStates.INGAME:
            return
        elif self.state == GameStates.INGAME and self.previous_state == GameStates.SETTINGS:
            return
        elif self.previous_state == GameStates.MENU and self.state == GameStates.SETTINGS:
            return
        elif self.previous_state == GameStates.SETTINGS and self.state == GameStates.MENU:
            return
        elif self.previous_state == GameStates.MENU and self.state == GameStates.MODS_LIST:
            return

        log('Stopping music...')
        self.stop_music()

        self.narrator.say(NARRATOR_GAMESTATE_TO_TAG[self.state])


    def set_title(self, title: str):
        """
        Set the game's caption.
        """
        assert type(title) == str, 'Window title must be string!'
        PROPERTIES = WindowProperties()
        PROPERTIES.setTitle(title)

        self.win.requestProperties(PROPERTIES)


    def new_task(self, name, function, is_lua: bool = False, args = None):
        """
        Create a new coroutine/task with the name `name` and task/function `function`.
        This function will be called every frame by Panda3D, TUO has no control over it's calling rate once it's hooked.

        !! WARNING !!

        The Task system is a single-threaded cycle-process! Do not call time.sleep or any other thread-pausing function on it!
        It will cause the entire Panda3D rendering system to freeze entirely!
        Instead, in order to block the task/coroutine, call Task.pause inside the task function!

        :: ARGS

        `name` :: The name of the function; required by Panda3D.
        `function` :: The function to be converted to a task/coroutine and called by Panda3D.
        """

        if is_lua:
            async def surrogate_task(task):
                result = function(task)

                # Programming TW: Heavy abuse of try clauses.
                # View at your own discretion.

                try:
                    await result
                except TypeError:
                    if result == task.done: return task.done

                return task.cont
            return self.taskMgr.add(surrogate_task, name, extraArgs=args)

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


    def get_state(self):
        """
        Give the state of the game.

        TUO.getState() -> `src.client.shared.GameStates`
        """
        return GameStates(self.state)


    def get_all_states(self):
        """
        Get a list of all game states, in case you cannot import the shared file because of a circular import.

        TUO.getAllStates() -> `src.client.shared.GameStates`
        """
        return self.states_enum


    def initialize_pbr_pipeline(self):
        """
        Initialize Tobspr's RenderPipeline for PBR.
        """
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
        start = time.perf_counter()

        log('Starting Discord RPC.', 'Worker/Startup')
        if self.rpc_manager != None:
            self.rpc_manager.run()

        self.update()

        if self.hardware_util.gl_version[0] == 4 and self.hardware_util.gl_version[1] > 2:
            log(f"This GPU does support OpenGL 4.3! [MAJOR={self.hardware_util.gl_version[0]};MINOR={self.hardware_util.gl_version[1]}]", "Worker/Hardware")
            if get_setting("video", "pbr") == True:
                log("Initializing tobspr's render pipeline! May the ricing begin!", "Worker/PBR")
                self.initialize_pbr_pipeline()
        else:
            warn(f"This GPU does not support OpenGL 4.3! [MAJOR={self.hardware_util.gl_version[0]};MINOR={self.hardware_util.gl_version[1]}]")
            settings = get_all_settings()
            settings['video']['pbr'] = False

            dump_setting(settings)

        # Create the events
        log('Creating all the events necessary for the game to function (on_state_change, on_exit, on_progress_screen_finish)', 'Worker/PostInit')
        self.create_event('on_state_change')
        self.create_event('on_start')
        self.create_event('on_exit')
        self.create_event('on_progress_screen_finish')

        # Initialize modding API
        if self.disable_mod_lvm == 0:
            self.mod_loader = ModLoader(self)
            self.mod_loader.load_mods()
            self.mod_loader.run_mods()
        else:
            warn('Modding API has been explicitly disabled.', 'Worker/Client')
            self.mod_loader = None

        # Start internal game handler
        self.game = Game(self, -1)
        self.get_event('on_start').fire([time.perf_counter() - start])
        log(f'Game has fully loaded up within {time.perf_counter() - start} ms.', 'Worker/start_internal_game')


    def quit(self):
        """
        Quit the internal managers, and tell Panda3D to stop the window.

        TUO.quit -> self.closeWindow <args=[win=self.win]>
                    self.finalizeExit
        """
        log("The Untold Odyssey is now stopping!", "Worker/Exit")
        self.narrator.say('gamestate.exit.enter')

        self.get_event('on_exit').fire()

        self.closeWindow(win=self.win)
        self.finalizeExit()

        # Patch: Make sure after this function is called, the exit is initialized immediately so that no malicious mod gets any time to do anything.
        exit(0)
