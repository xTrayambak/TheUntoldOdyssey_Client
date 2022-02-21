from src.log import *
from src.client.game.entitymanager import EntityManager

class Game:
    def __init__(self):
        self.entityManager = EntityManager()

    def add_new_entity(self, entity):
        self.entityManager.add_entity(entity)