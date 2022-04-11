from src.client.loader import getAsset

_cat_type = [
    'songs',
    'sounds'
]

class AudioLoader:
    def __init__(self, instance):
        self.instance = instance
    
    def load(self, category_type: int, name: str):
        if category_type > 1:
            raise ValueError("Category type cannot be greater than 2! Malformed value provided.")
        
        path = getAsset(_cat_type[category_type], name)

        if _cat_type[category_type] == 'songs':
            path = path['path']

        return self.instance.loader.loadSfx(
            path
        )