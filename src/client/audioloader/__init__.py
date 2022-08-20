from src.client.loader import getAsset
from src.client.types.audio import Audio

_cat_type = [
    'songs',
    'sounds'
]

class AudioLoader:
    def __init__(self, instance):
        self.instance = instance
        self.sounds = []
    
    def load(self, path: str):
        audio = Audio(path, self.instance)
        self.sounds.append(audio)

        return audio

    def load_path(self, path: str):
        audio = self.instance.loader.loadSfx(path)
        self.sounds.append(audio)

        return audio

    def stop_all_sounds(self):
        for sound in self.sounds: sound.stop()
