#!/usr/bin/env python3
class GameHandler:
    def __init__(self):
        from src.client.libinstaller import installAllLibraries

        #installAllLibraries()

        from src.client import TUO

        self.tuo = TUO()

    def run(self):
        """
        GameHandler.run() -> self.tuo.run()
                          -> self.tuo.start_internal_game()

        ===== CONVENIENCE FUNCTION TO START A GAME INSTANCE =====
        """
        self.tuo.workspace.init(self.tuo)
        self.tuo.start_internal_game()
        self.tuo.run()
        #self.tuo.quit()

if __name__ == "__main__":
    game = GameHandler()
    game.run()