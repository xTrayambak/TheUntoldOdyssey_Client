from src.client.loader import getAsset
from src.log import log, warn


class FontLoader:
    def __init__(self, instance):
        self.instance = instance
        self.cache = {}

    def get(self, name: str):
        if name in self.cache: return self.cache[name]

        return None

    def load(self, name, loadFromCache = True):
        """
        Load a font into memory for usage.

        :: ARGS ::
        `name` :: The name of the font to be called by the TUO asset loader.
        `loadFromCache` :: If this is set to [True]; then a cached version of the font will be loaded, if found. This can help speed up the loading cycle.
        
        !! WARNING !!
        DO NOT TOUCH `loadFromCache` IF YOU DON'T KNOW WHAT YOU'RE DOING! IF YOU SET IT TO FALSE THE PERFORMANCE MAY DROP, BUT CACHED FONTS MAY HAVE SOME ISSUES.
        """

        if name in self.cache and loadFromCache: 
            return self.cache[name]

        font = self.instance.loader.loadFont(
            getAsset("fonts", name)
        )

        self.cache.update({name: font})

        log("Loaded font [{}] and cached into memory.".format(name), "Worker/FontLoader")
        
        return font