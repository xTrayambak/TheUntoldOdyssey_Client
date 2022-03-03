from src.log import *
from src.client.loader import getAsset

import json
import random
import math

class Chunk:
    SIZE_X = 32
    SIZE_Y = 32
    SIZE_Z = 16

sin_val = 0

class MapLoader:
    def __init__(self, instance) -> None:
        self.objectsFile = json.load(
            open(getAsset("mapobjects", "path"), "r")
        )

        self.instance = instance

    def chunkLoaderTask(self):
        for x in range(8):
            for y in range(8):
                map = self.instance.objectLoader.loadObject(
                    "chunk_test"
                )

                map.setShader(
                    self.instance.workspace.objects["shaders"][1]["shader"]
                )

                map.setPos(
                    (x*Chunk.SIZE_X, y*Chunk.SIZE_Y, 0)
                )

    def load(self):
        self.chunkLoaderTask()
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