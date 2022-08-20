#!/usr/bin/env python3

import os
import pathlib
import argparse
import sys

DEFAULT_MEM = 1500

VERSION = "0.1.5-dev2" #NOTE TO DEVELOPERS: MAKE SURE TO CHANGE THIS AS THE VERSION INCREASES, THIS IS NECESSARY SO THE CLIENT CAN LOCATE IT'S PROPER WORKING DIRECTORY.

class GameHandler:
    """
    The entire backbone class of the TUO instance -- patches the game for different systems, installs required libraries, and acts as an intermediary between
    the TUO class and the raw CLI arguments.
    """
    def __init__(self, max_mem: int = DEFAULT_MEM, token: str = None, disable_gc: int = 0, disable_logging: int = 0, disable_mod_lvm: int = 0, gc_routine_delay: int = 120):
        from src.libinstaller import installAllLibraries
        from src.libtraceback import log_traceback
        from src.log import log, set_enabled

        log(f"PVM Environment: [{sys.executable}]")
 
        import gc
        if disable_gc == 0:
            gc.enable()
        else:
            gc.disable()

        set_enabled(disable_logging)

        if os.path.exists("LAUNCHER_ENVIRONMENT"):
            log("Patching directory...")
            entire_path = str(pathlib.Path(__file__))
            client_path = ""

            log(f"Full path to client startup file is [{entire_path}]")

            for dirName in entire_path.split('/'):
                client_path += dirName + '/'
                if dirName == VERSION:
                    break

            """if sys.platform == 'linux':
                log("Setting client data path to ["+client_path+"]", "ClientPathDEBUG")
                os.chdir(client_path)
                log("Client working directory patch completed!", "ClientDirectoryWorkaround")"""

        log("Trying to find any libraries that need to be installed.", "Worker/Bootstrap")
        installAllLibraries()

        if os.path.exists("DEBUG_MODE"):
            log("Library installation process complete.", "Worker/Bootstrap")
            log("Pre-bootup client initialization complete, now changing into client mode.")
            from src.client import TUO
            from src.client.gcroutine import GC
            log("Changed into client mode. Now, the client code is going to be run.")

            self.tuo = TUO(max_mem, token, disable_mod_lvm)

            if disable_gc == 0:
                gc_module = GC(self)
                gc_module.set_delay(gc_routine_delay)
                self.tuo.add_module(gc_module)

            self.tuo.enableParticles()
        else:
            try:
                log("Library installation process complete.", "Worker/Bootstrap")
                log("Pre-bootup client initialization complete, now changing into client mode.")
                from src.client import TUO
                log("Changed into client mode. Now, the client code is going to be run.")
                self.tuo = TUO(max_mem, token, disable_mod_lvm)

                if disable_gc == 0:
                    gc_module = GC(self)
                    gc_module.set_delay(gc_routine_delay)
                    self.tuo.add_module(gc_module)

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
            self.get_instance().start_internal_game()
            self.get_instance().workspace.init(self.tuo)
            self.get_instance().run()
        else:
            try:
                self.get_instance().start_internal_game()
                self.get_instance().workspace.init(self.tuo)
                self.get_instance().run()
            except Exception as e:
                log(f"Caught exception whilst running game: {str(e)}", "GameHandler/Run")
                log_traceback(self.tuo)
                exit(1)

        exit(0)

if __name__ == "__main__":
    mem_max = None
    token = None

    argparser = argparse.ArgumentParser(description='Run "The Untold Odyssey" client.')
    argparser.add_argument(
        '--gc',
        metavar = '-g',
        type = int,
        help = 'Whether or not to perform manual GC routines and to also disable the automatic GC schedule of the interpreter.',
        action = 'store',
        required = False,
        default = 0
    )
    argparser.add_argument(
        '--token',
        metavar = '-t',
        type = str,
        help = 'The Syntax Studios account token.',
        action = 'store',
        required = False
    )
    argparser.add_argument(
        '--log',
        metavar = '-l',
        type = int,
        help = 'Whether or not to use logging (default = 0/yes)',
        action = 'store',
        required = False,
        default = 0
    )
    argparser.add_argument(
        '--lvm',
        '--m',
        type = int,
        help = 'Whether or not to enable the modding API (default = 0/yes)',
        action = 'store',
        required = False,
        default = 0
    )
    argparser.add_argument(
        '--gc-delay',
        '-gcd',
        type = float,
        help = 'The delay at which the GC routine runs (default = 120)',
        action = 'store',
        required = False,
        default = 120
    )

    args = argparser.parse_args()
    
    disable_gc = args.gc
    token = args.token
    disable_logging = args.log
    disable_mod_lvm = args.lvm
    gc_routine_delay = args.gc_delay


    if not isinstance(mem_max, int):
        mem_max = DEFAULT_MEM

    if not isinstance(token, str):
        token = 'no-tok-provided'

    game = GameHandler(mem_max, token, disable_gc, disable_logging, disable_mod_lvm, gc_routine_delay)
    game.run()
