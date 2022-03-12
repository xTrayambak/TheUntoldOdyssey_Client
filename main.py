#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import pathlib
import sys
from multiprocessing.pool import ThreadPool

argparser = ArgumentParser(
    description = "Run The Untold Odyssey."
)

DEFAULT_MEM = 1500

argparser.add_argument("memory", 
                        metavar = "m",
                        type = int,
                        help = f"The maximum amount of memory the game can use. (Defaults to {DEFAULT_MEM} MB)",
                        const = DEFAULT_MEM,
                        nargs = "?"
)

argparser.add_argument(
    "token",
    metavar = "t",
    type = str,
    help = f"The Syntax Studios account token.",
    const = "",
    nargs = "?"
)

VERSION = "0.1.1" #NOTE TO DEVELOPERS: MAKE SURE TO CHANGE THIS AS THE VERSION INCREASES, THIS IS NECESSARY SO THE CLIENT CAN LOCATE IT'S PROPER WORKING DIRECTORY.

class GameHandler:
    def __init__(self, max_mem: int = DEFAULT_MEM, token: str = 'no-token-provided'):
        from src.libinstaller import installAllLibraries
        from src.libtraceback import log_traceback
        from src.log import log

        log(f"PVM Environment: [{sys.executable}]")
        
        if not os.path.exists("DEBUG_MODE"):
            log("Patching directory...")
            entire_path = str(pathlib.Path(__file__))
            client_path = ""
            
            log(f"Full path to client startup file is [{entire_path}]")
            
            for dirName in entire_path.split("/"):
                client_path += dirName + "/"
                if dirName == VERSION:
                    break
            
            log("Setting client data path to ["+client_path+"]", "ClientPathDEBUG")
            os.chdir(client_path)
            log("Client working directory patch completed! Fuck you POSIX! 🖕", "ClientDirectoryWorkaround")
            
        log("Trying to find any libraries that need to be installed.", "Worker/Bootstrap")
        installAllLibraries()

        if os.path.exists("DEBUG_MODE"):
            log("Library installation process complete.", "Worker/Bootstrap")
            log("Pre-bootup client initialization complete, now changing into client mode.")
            from src.client import TUO
            from src.client.linuxpatcher import patch
            log("Changed into client mode. Now, the client code is going to be run.")
            if sys.platform == 'linux':
                log("Running Linux patches...")
                patch()
                
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
                exit(1)

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
            self.tuo.start_internal_game()
            self.tuo.workspace.init(self.tuo)
            self.tuo.run()
        else:
            try:
                self.tuo.start_internal_game()
                self.tuo.workspace.init(self.tuo)
                self.tuo.run()
            except Exception as e:
                log(f"Caught exception whilst running game: {str(e)}", "GameHandler/Run")
                log_traceback(self.tuo)
                exit(1)

        exit(0)

if __name__ == "__main__":
    args = argparser.parse_args()
    mem_max = args.memory
    token = args.token
    if mem_max == None: mem_max = DEFAULT_MEM
    if token == None: token = "no-tok-provided"

    game = GameHandler(mem_max, token)
    game.run()