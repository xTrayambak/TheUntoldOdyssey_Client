#!/usr/bin/env python3

"""
Managed class for the game's window and running everything, including the workspace, every entity and
networking.

Very good already, doesn't need too much refactoring later. Proud of this.
"""
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import loadPrcFile
from pandac.PandaModules import WindowProperties
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import ClockObject

from src.client.log import log
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

import gc

VERSION = open("VER").read()

PROPERTIES = WindowProperties()
PROPERTIES.setTitle("The Untold Odyssey {}".format(VERSION))

class TUO(ShowBase):
    def __init__(self, memory_max: int = 5000):
        log(f"The Untold Odyssey {VERSION} loaded up!")
        log("Initializing Panda3D rendering engine.")
        loadPrcFile("assets/config.prc")
        ShowBase.__init__(self)
        log("Panda3D initialized.")

        ### START DEFINING VARIABLES ###
        self.state = GameStates.MENU
        self.workspace = Workspace()
        self.ambienceManager = AmbienceManager()
        self.inputManager = InputManager(self)
        self.networkClient = NetworkClient()
        self.rpcManager = None

        try:
            self.rpcManager = RPCManager(self)
        except Exception as exc:
            log(f"Failed to initialize Discord rich presence. [{exc}]")

        self.fontLoader = FontLoader(self)
        self.textureLoader = TextureLoader(self)
        self.objectLoader = ObjectLoader(self)
        self.syntaxUtil = SyntaxUtil(self)
        self.player = Player(self, "player", "player")

        self.states_enum = GameStates
        self.max_mem = memory_max

        self.version = VERSION
        self.wireframeIsOn = False
        self.fpsCounterIsOn = False
        self.inputManager.init()
        self.inputManager.hook()

        self.syntaxUtil.hook()

        self.filters = CommonFilters(self.win, self.cam)

        self.filtersSupported = self.filters.setCartoonInk()

        warn(f"Are graphics pipeline filters supported? [{self.filtersSupported}]")

        self.globalClock = ClockObject.getGlobalClock()

        self.win.requestProperties(PROPERTIES)

    def poll(self, task):
        raise NotImplementedError("Not implemented yet; wait.")

    def change_state(self, state: int):
        """
        Change the game's story/part "state"; basically tell the game at which point of gameplay it should switch to.
        Eg. menu, loading screen, in-game or connecting screen.

        This is controlled by an Enum, feel free to change it anytime as nothing too technical changes with it.
        Why am I writing docs? Oh wait, yeah, this will probably be open source so 7 year old script kiddies don't accuse
        me of integrating trackers or a Bitcoin miner into the game.
        """
        self.state = GameStates(state)
        self.update()

        PROPERTIES = WindowProperties()
        PROPERTIES.setTitle("The Untold Odyssey {} | {}".format(VERSION, GAMESTATES_TO_STRING[self.state]))

        self.win.requestProperties(PROPERTIES)

        self.ambienceManager.stop_all_tracks()

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
                obj.destroy()
            except AttributeError:
                obj.removeNode()

        gc.collect()

    def update(self):
        """
        Updates the game state manager.

        TUO.update() -> state_execution[state] <args=self (TUO instance)>
        """
        GAMESTATE_TO_FUNC[self.state](self)

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

    def quit(self):
        """
        Quit the internal managers, and tell Panda3D to stop the window.

        TUO.quit -> self.closeWindow <args=[win=self.win]>
                    self.finalizeExit
        """
        self.ambienceManager.running = False
        self.closeWindow(win=self.win)
        self.finalizeExit()