from src.client.loader import getAsset
from src.log import log, warn


class TextureLoader:
    def __init__(self, instance):
        self.instance = instance

        self.cache = {

        }

    def loadTexture(self, path: str, loadCache: bool = True):
        if path in self.cache and loadCache: return self.cache[path]

        texture = self.instance.loader.loadTexture(
            path
        )

        self.cache[path] = texture

        return texture