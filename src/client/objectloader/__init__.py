from src.log import log, warn
from src.client.loader import getAsset

class ObjectLoader:
    def __init__(self, instance):
        self.instance = instance

        self.cache = {

        }

    def loadObject(self, name, texture: str = None, loadFromCache: bool = True):
        if name in self.cache and loadFromCache: return self.cache[name]

        path = getAsset("models", name)["path"]

        log(f"Loading 3D model '{name}' ({path})")

        model = self.instance.loader.loadModel(path)

        if texture != None:
            model.setTexture(
                self.instance.textureLoader.loadTexture(
                    texture
                )
            )

        model.reparentTo(self.instance.render)

        self.cache.update({name: model})

        return model
