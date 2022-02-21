from src.log import *
from src.client.game.entity import Entity

class EntityManager:
    def __init__(self):
        self.entities = []
        self.entity_count = 0

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        self.entity_count += 1