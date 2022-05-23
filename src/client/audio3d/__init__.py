from src.log import *
from direct.showbase import Audio3DManager
from panda3d.core import NodePath

class Audio3D:
    def __init__(self, instance):
        self.tuo = instance
        self.a3d_mgr = Audio3DManager.Audio3DManager(instance.sfxManagerList[0], instance.cam)
    
    def summon_new_source(self, sound: str, object: NodePath):
        self.a3d_mgr.attachSoundToObject(self.tuo.audioLoader.load_path(sound), object)