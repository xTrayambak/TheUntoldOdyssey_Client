from src.client.vfxmanager.parser import parse
from src.client.vfxmanager.pipeline import Pipeline
from src.log import log, warn


class VFXManager:
    def __init__(self, instance = None) -> None:
        self.pipeline = Pipeline(instance)
    
    def load_file(self, file):
        self.pipeline.execute(parse(file))