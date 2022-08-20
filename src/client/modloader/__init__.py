import os
import time
import copy

from src.log import log, warn
from src.client.lvm import VM

# webapi
import requests

# os module inside LUA
import os
import sys
import time
import datetime

# math
import math
import random
from src.libs.noise.perlin import SimplexNoise

class Mod:
    def __init__(self, name: str, version: str, files: list, modloader, tuo):
        self.name = name
        self.files = files
        self.modloader = modloader
        self.version = version
        self.tuo = tuo
        self.suspicious = False

        log(f'Mod "{name}" initialized.', 'Worker/ModLoader')

    def set_suspicious(self, value: bool = True): self.suspicious = value

    def add_file(self, file: str):
        self.files.append(file)

    def run(self):
        start_time = time.perf_counter()
        log(f'Mod "{self.name}" is now running.')
        for file in self.files:
            res = self.modloader.lvm.run(file)
            log(f'Loaded file "{file}"', f'Worker/Mod/{self.name}')

            if res == 'terminate-unsafe': return res

        log(f'Mod loaded successfully within {time.perf_counter() - start_time} ms.', f'Worker/Mod/{self.name}')

class ModLoader:
    def __init__(self, tuo, mods_path: str = 'mods'):
        log(f'Mod loader starting. Path to search is set to "{mods_path}"', 'Worker/ModLoader')
        self.mods_path = mods_path

        log(f'Starting LUA VM.', 'Worker/ModLoader')
        self.lvm = VM()
        log(f'LVM {self.lvm.runtime.lua_version[0]}.{self.lvm.runtime.lua_version[1]} has started successfully.', 'Worker/ModLoader')
        self.tuo = tuo

        # Inject variables required for most mods to work (`tuo` table) and remove `python` table.

        self.lvm.globals().tuo = {
            'client': tuo
        }

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
            'tags': ['SANDBOXED', 'OFFICIAL_MODDING_API_LVM']
        }

        # I/O and direct access to Python is scary. Let's *NOT* give it to them.
        self.lvm.globals().python = None
        self.lvm.globals().io = None
        self.lvm.globals().math = {
            'sin': math.sin,
            'acos': math.acos,
            'cos': math.cos,
            'ceil': math.ceil,
            'floor': math.floor,
            'pi': math.pi,
            'gamma': math.gamma,
            'random': random.randint
        }

        smplx_n = SimplexNoise()

        self.lvm.globals().math.update({'noise2': smplx_n.noise2, 'noise3': smplx_n.noise3})

        self.mods = []

        if not os.path.exists(mods_path):
            warn('Mods path to search does not exist. Mods will not be loaded.', 'Worker/ModLoader')
            return

        if os.path.isfile(mods_path):
            warn('Mods path to search is a file, not a directory. Mods will not be loaded.', 'Worker/ModLoader')
            return

    def run_mods(self):
        for mod in self.mods:
            result = mod.run()

            if result == 'terminate-unsafe':
                warn(f'Flagging mod "{mod.name}" as suspicious, blocking execution and warning the user.')
                mod.set_suspicious()
                self.tuo.warn('Unsafe modification detected.', f'We have detected that the mod "{mod.name}" you have installed\nis performing malicious activity.\nPlease discard the mod as soon as possible.\nIf you believe this is a false positive,\nplease report it to the Syntax Studios developers.')

    def load_mods(self):
        log('Searching for mods.', 'Worker/ModLoader')
        mods_path = self.mods_path

        for mod_dir in os.listdir(mods_path):
            if not os.path.isfile(mods_path + '/' + mod_dir + '/TUO_MOD'): warn(f'Found a directory that is not a TUO mod ("{mod_dir}"), please consider not littering your mods directory with random folders to maintain uniformity.', 'Worker/ModLoader'); continue

            try:

                with open(mods_path + '/' + mod_dir + '/TUO_MOD', 'r') as mf:
                    metadata = mf.readlines()

                    modname = metadata[0].split('\n')[0]
                    version = metadata[1].split('\n')[0]
            except IndexError:
                warn(f'The metadata file for "{mod_dir}" is corrupted or outdated as some headers are missing.', 'Worker/ModLoader')
                continue

            mod = Mod(modname, version, [], self, self.tuo)

            for file in os.listdir(mods_path + '/' + mod_dir):
                if not os.path.isfile(mods_path + '/' + mod_dir + '/' + file) or not file.endswith('.lua'): continue
                log(f'Found LUA file "{mods_path}/{mod_dir}/{file}"', 'Worker/ModLoader')
                mod.add_file(mods_path + '/' + mod_dir + '/' + file)
                self.mods.append(mod)
