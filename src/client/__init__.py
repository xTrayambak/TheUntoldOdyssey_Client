#!/usr/bin/env python3

"""
Managed class for the game's window and running everything, including the workspace, every entity and
networking.

Very good already, doesn't need too much refactoring later. Proud of this.
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from pandac.PandaModules import WindowProperties

from src.client.log import log
from src.client.shared import *
from src.client.workspace import Workspace
from src.client.managers.ambience import AmbienceManager
from src.client.managers.input import InputManager
from src.client.networking import NetworkClient
from src.client.managers.presence import RPCManager

import gc

VERSION = open("VER").read()

PROPERTIES = WindowProperties()
PROPERTIES.setTitle("The Untold Odyssey {}".format(VERSION))

class TUO(ShowBase):
    def __init__(self):
        log(f"The Untold Odyssey {VERSION} loaded up!")
        log("Initializing Panda3D rendering engine.")
        loadPrcFile("assets/config.prc")
        ShowBase.__init__(self)
        log("Panda3D initialized.")

        ### START DEFINING VARIABLES ###
        self.state = GameStates.MENU
        self.workspace = Workspace()
        self.ambienceManager = AmbienceManager()
        self.inputManager = InputManager()
        self.networkClient = NetworkClient()
        self.rpcManager = RPCManager(self)

        self.states_enum = GameStates

        self.version = VERSION
        self.wireframeIsOn = False
        self.inputManager.hook(self)

        self.win.requestProperties(PROPERTIES)

    def add_ui_component(self, component):
        self.ui.append(component)

    def remove_all_ui_components(self):
        for component in self.ui:
            component.destroy()

    def change_state(self, state: int):
        self.state = GameStates(state)
        self.update()

    def clear(self):
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