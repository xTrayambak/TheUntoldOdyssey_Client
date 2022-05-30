from src.client.game.entitymanager import EntityManager
from src.log import *


class Game:
    def __init__(self):
        self.entityManager = EntityManager()

        self.isFightingBoss = False
        self.bossID = None
        self.players = {}

    def setPlayers(self, plr_list: dict):
        self.players = plr_list

    def getPlayers(self):
        return self.players
    
    def bossFightInProgress(self) -> bool:
        return self.isFightingBoss

    def setBossFightInProgress(self, value: bool, bossID: int = None):
        if value:
            if not bossID:
                warn(f"No boss ID was provided! Must be a malformed packet. Abort!", "setBossFightInProgress")
                raise Exception("Expected int as bossID, but got no argument for it instead.")
            
            if type(bossID) != int:
                warn(f"The boss ID is of incorrect type! ({type(bossID)})", "setBossFightInProgress")
                raise TypeError(f"The boss ID is of incorrect type! Expected int; got {type(bossID)}")

            log(f"Boss fight is beginning. [BOSSID={bossID}]", "setBossFightInProgress")
            self.isFightingBoss = value
            self.bossID = bossID
        else:
            log("Boss fight has stopped.", "setBossFightInProgress")

            self.isFightingBoss = False
            self.bossID = None

    def getBID(self) -> int | None:
        return self.bossID

    def add_new_entity(self, entity):
        self.entityManager.add_entity(entity)