from src.log import *
from src.client.loader import getAsset

import json

class MapLoader:
    def __init__(self, instance) -> None:
        self.objectsFile = json.load(
            open(getAsset("mapobjects", "path"), "r")
        )

        self.instance = instance

    def load(self):
        for obj in self.objectsFile:
            name = obj["name"]
            position = obj["position"]

            position = (position[0], position[1], position[2])

            texture = obj["texture"]
            model = obj["model"]
            hpr = obj["hpr"]

            renderModel = self.instance.objectLoader.loadObject(
                model, texture
            )

            renderModel.setHpr(
                hpr[0], hpr[1], hpr[2]
            )