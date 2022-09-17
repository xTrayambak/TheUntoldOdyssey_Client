from src.client.game.entitymanager import EntityManager
from src.log import *
from src.client.module import Module, ModuleCodes
from src.client.lvm import VM
from src.libs.noise.perlin import SimplexNoise
from src.client.objects import Object

import math
import requests
import time
import datetime
import json
import os
import random
import direct
import panda3d

def _lvm_json_load(file: str):
    with open(file, 'r') as file: return json.load(file)

def _lvm_json_dump(file: str, data):
    if isinstance(data, bytes): warn('_lvm_json_dump(): Ignored request as data is bytes.')

    with open(file, 'w') as file: return json.dump(data, file)

def _lvm_rand_choice(seq: list):
    _seq_py = []

    for idx in seq:
        _seq_py.append(seq[idx])

    return random.choice(_seq_py)

def _lvm_free_obj(obj: object):
    del obj

INTERNAL_JSON_FUNCTIONS_LVM = {
    'load': _lvm_json_load,
    'dump': _lvm_json_dump
}


class Game:
    """
    The `Game` class, handles everything that is going on in the game during a play session.
    """
    def __init__(self, tuo, game_type: int, extra_data: dict = None):
        self.entity_manager = EntityManager()

        self.isFightingBoss = False
        self.bossID = None
        self.players = {}
        self.tuo = tuo

        self.dimension_enum = tuo.getSharedData().DIMENSION
        self.lvm = VM()

        # Begin sandbox, in case the game logic files have been tampered with.
        self.lvm.globals().io = None
        self.lvm.globals().python = None
        self.lvm.globals().web = {
            'get': requests.get,
            'post': requests.post
        }

        self.lvm.globals().os = {
            'time': time.time,
            'time_ns': time.time_ns,
            'perf_counter': time.perf_counter,
            'python_version': sys.version,
            'platform': sys.platform,
            'tags': ['SANDBOXED', 'GAME_INTERNAL_LVM']
        }

        self.lvm.globals().tuo = tuo
        self.lvm.globals().json = INTERNAL_JSON_FUNCTIONS_LVM

        n = SimplexNoise()
        self.lvm.globals().math = {
            'gamma': math.gamma,
            'pi': math.pi,
            'noise2': n.noise2,
            'noise3': n.noise3,
            'sin': math.sin,
            'floor': math.floor,
            'ceil': math.ceil,
            'cos': math.cos,
            'cosh': math.cosh,
        }

        self.lvm.globals().random = {
            'new': random.Random,
            'randint': random.randint,
            'randrange': random.randrange,
            'choice': _lvm_rand_choice
        }

        self.lvm.globals().audio_loader = tuo.audio_loader
        self.lvm.globals().font_loader = tuo.fontLoader
        self.lvm.globals().texture_loader = tuo.texture_loader
        self.lvm.globals().Object = Object
        self.lvm.globals().image_loader = tuo.image_loader
        self.lvm.globals().direct = direct
        self.lvm.globals().panda = panda3d
        self.lvm.globals().free = _lvm_free_obj

        self.game_type = game_type

        if game_type == 0:
            # local/singleplayer session
            self.extra_data = extra_data

            #self.savedata = extra_data['savefiles']

        self.dimension = None
        log('Loading LUA game logic.', 'Worker/Game')
        self.load_lua_scripts()

    def get_players(self):
        """
        Get all the players in this world.
        """
        return self.players

    def load_lua_script(self, path: str):
        """
        Load a .lua script
        """
        self.lvm.run(path)

    def load_lua_scripts_in_dir(self, path: str):
        """
        Load all .lua scripts in a specified directory.
        """
        for path in os.listdir('src/client/game/logic/'+path+'/'):
            if os.path.isdir(path):
                # Haha, recursion go brrrrr.
                # (Hopefully) nobody is running the game on a Raspberry Pi Pico.
                self.load_lua_scripts_in_dir('src/client/game/logic/'+path)

            if not path.endswith('.lua'): continue
            self.load_lua_script('src/client/game/logic/'+path)

    def load_lua_scripts(self):
        """
        Load all the .lua game logic.
        """
        for path in os.listdir('src/client/game/logic/'):
            if os.path.isdir(path): self.load_lua_scripts_in_dir(path)
            if not path.endswith('.lua'): continue

            self.load_lua_script('src/client/game/logic/'+path)

    def boss_fight_in_progress(self) -> bool:
        """
        Determines whether a boss fight is in progress.
        """
        return self.isFightingBoss

    def get_boss_id(self) -> int | None:
        """
        Get the bosses currently loaded in
        """
        return self.bossID

    def add_new_entity(self, entity):
        """
        Add a new entity.
        """
        self.entity_manager.add_entity(entity)

    def get_dimension(self): 
        """
        TODO: What.
        """
        if self.game_type == 0:
            return self.dimension
