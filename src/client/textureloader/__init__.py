from src.client.loader import getAsset
from src.log import log, warn


class TextureLoader:
    def __init__(self, instance):
        self.instance = instance

        self.cache = {

        }

    def load_texture(self, path: str, loadCache: bool = True):
        """
        Load up a texture.
        """
        if path in self.cache and loadCache: return self.cache[path]

        texture = self.instance.loader.loadTexture(
            path
        )

        self.cache[path] = texture

        return texture

    def loadTexture(self, *args): 
        """
        Load up a texture.

        **WARNING**: This may be deprecated in a future release as this function is a violation of PEP-8. Please use
        TextureLoader.load_texture() instead.
        """ 
        return self.load_texture(*args)
