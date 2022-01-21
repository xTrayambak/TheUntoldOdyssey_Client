#!/usr/bin/env python3

from argparse import ArgumentParser
import os

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

class GameHandler:
    def __init__(self, max_mem: int = DEFAULT_MEM):
        from src.libinstaller import installAllLibraries
        from src.libtraceback import log_traceback
        from src.log import log
        
        log("Trying to find any libraries that need to be installed.", "Worker/Bootstrap")
        installAllLibraries()
        
        try:
            log("Library installation process complete.", "Worker/Bootstrap")
            log("Pre-bootup client initialization complete, now changing into client mode.")
            from src.client import TUO
            log("Changed into client mode. Now, the client code is going to be run.")
            self.tuo = TUO(max_mem)
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
            self.tuo.workspace.init(self.tuo)
            self.tuo.start_internal_game()
            self.tuo.run()
        else:
            try:
                self.tuo.workspace.init(self.tuo)
                self.tuo.start_internal_game()
                self.tuo.run()
            except Exception as e:
                log(f"Caught exception whilst running game: {str(e)}", "GameHandler/Run")
                log_traceback(self.tuo)
                exit(1)

        exit(0)

if __name__ == "__main__":
    args = argparser.parse_args()
    mem_max = args.memory
    if mem_max == None: mem_max = DEFAULT_MEM

    game = GameHandler(mem_max)
    game.run()