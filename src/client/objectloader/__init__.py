from src.client.log import *
from src.client.loader import getAsset

class ObjectLoader:
    def __init__(self, instance):
        self.instance = instance

        self.cache = {

        }

    def loadObject(self, name, subcategory: str = None, loadFromCache: bool = True):
        if name in self.cache and loadFromCache: return self.cache[name]

        path = getAsset("models", subcategory)[name]["path"]

        log(f"Loading 3D model '{name}' ({path})")

        model = self.instance.loader.loadModel(path)

        self.cache.update({name: model})

        return model
