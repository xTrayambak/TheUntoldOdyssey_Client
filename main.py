#!/usr/bin/env python3

import os
import pathlib
import sys

DEFAULT_MEM = 1500

VERSION = "0.1.5-dev1" #NOTE TO DEVELOPERS: MAKE SURE TO CHANGE THIS AS THE VERSION INCREASES, THIS IS NECESSARY SO THE CLIENT CAN LOCATE IT'S PROPER WORKING DIRECTORY.

class GameHandler:
    """
    The entire backbone class of the TUO instance -- patches the game for different systems, installs required libraries, and acts as an intermediary between
    the TUO class and the raw CLI arguments.
    """
    def __init__(self, max_mem: int = DEFAULT_MEM, token: str = 'no-token-provided'):
        from src.libinstaller import installAllLibraries
        from src.libtraceback import log_traceback
        from src.log import log

        log(f"PVM Environment: [{sys.executable}]")

        if os.path.exists("LAUNCHER_ENVIRONMENT"):
            log("Patching directory...")
            entire_path = str(pathlib.Path(__file__))
            client_path = ""

            log(f"Full path to client startup file is [{entire_path}]")

            for dirName in entire_path.split('/'):
                client_path += dirName + '/'
                if dirName == VERSION:
                    break

            log("Setting client data path to ["+client_path+"]", "ClientPathDEBUG")
            os.chdir(client_path)
            log("Client working directory patch completed!", "ClientDirectoryWorkaround")

        log("Trying to find any libraries that need to be installed.", "Worker/Bootstrap")
        installAllLibraries()

        if os.path.exists("DEBUG_MODE"):
            log("Library installation process complete.", "Worker/Bootstrap")
            log("Pre-bootup client initialization complete, now changing into client mode.")
            from src.client import TUO
            log("Changed into client mode. Now, the client code is going to be run.")

            self.tuo = TUO(max_mem, token)
            self.tuo.enableParticles()
        else:
            try:
                log("Library installation process complete.", "Worker/Bootstrap")
                log("Pre-bootup client initialization complete, now changing into client mode.")
                from src.client import TUO
                log("Changed into client mode. Now, the client code is going to be run.")
                self.tuo = TUO(max_mem, token)
                self.tuo.enableParticles()
            except Exception as exc:
                log(f"An error occured whilst initializing the game. [{exc}]")
                log_traceback()
                log('Initializing PDB.', 'Worker/PostMortem')

                import pdb
                pdb.main()
                exit(1)

    def getInstance(self):
        """
        Get the current running instance of TUO.
        """
        return self.tuo

    def get_instance(self):
        """
        Get the current running instance of TUO.
        """
        return self.tuo

    def run(self):
        """
        GameHandler.run() -> self.tuo.run()
                          -> self.tuo.start_internal_game()

        ===== CONVENIENCE FUNCTION TO START A GAME INSTANCE =====
        """
        from src.libtraceback import log_traceback
        from src.log import log, warn
        if os.path.exists("DEBUG_MODE"):
            warn("The Untold Odyssey: DEBUG MODE")
            self.getInstance().start_internal_game()
            self.getInstance().workspace.init(self.tuo)
            self.getInstance().run()
        else:
            try:
                self.getInstance().start_internal_game()
                self.getInstance().workspace.init(self.tuo)
                self.getInstance().run()
            except Exception as e:
                log(f"Caught exception whilst running game: {str(e)}", "GameHandler/Run")
                log_traceback(self.tuo)
                exit(1)

        exit(0)

if __name__ == "__main__":
    mem_max = None
    token = None

    if len(sys.argv) > 1:
        mem_max = sys.argv[0]
    if len(sys.argv) > 2:
        token = sys.argv[1]

    if not isinstance(mem_max, int):
        mem_max = DEFAULT_MEM

    if not isinstance(token, str):
        token = 'no-tok-provided'

    game = GameHandler(mem_max, token)
    game.run()
