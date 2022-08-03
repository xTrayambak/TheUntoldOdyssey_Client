from src.client.loader import getAsset
from src.client.types.audio import Audio

_cat_type = [
    'songs',
    'sounds'
]

class AudioLoader:
    def __init__(self, instance):
        self.instance = instance
    
    def load(self, path: str):
        return Audio(path, self.instance)

    def load_path(self, path: str):
        return self.instance.loader.loadSfx(path)
