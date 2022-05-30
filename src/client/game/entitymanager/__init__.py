from src.client.game.entity import Entity
from src.log import *


class EntityManager:
    def __init__(self):
        self.entities = []
        self.entity_count = 0

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        self.entity_count += 1