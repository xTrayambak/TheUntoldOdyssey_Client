#!/usr/bin/env python3

from argparse import ArgumentParser

argparser = ArgumentParser(
    description = "Run The Untold Odyssey."
)
argparser.add_argument("max_mem_usage", 
                        metavar = "m",
                        type = int,
                        help = "The maximum amount of memory the game can use. (Defaults to 800 MB)",
                        const = 800,
                        nargs = "?"
)

class GameHandler:
    def __init__(self, max_mem: int = 800):
        from src.libinstaller import installAllLibraries

        installAllLibraries()

        from src.client.libtraceback import log_traceback
        from src.client import TUO
        from src.client.log import log

        try:
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
        from src.client.libtraceback import log_traceback
        from src.client.log import log
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
    mem_max = args.max_mem_usage

    game = GameHandler(mem_max)
    game.run()