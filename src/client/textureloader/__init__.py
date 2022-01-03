from src.client.log import *
from src.client.loader import getAsset

class TextureLoader:
    def __init__(self, instance):
        self.instance = instance

        self.cache = {

        }

    def loadTexture(self, name: str, loadCache: bool = True):
        if name in self.cache and loadCache: return self.cache[name]

        texture = self.instance.loader.loadTexture(
            getAsset("textures", name)["path"]
        )

        self.cache[name] = texture

        return texture