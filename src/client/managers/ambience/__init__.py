#!/usr/bin/env python3
from direct.task import Task
from src.client.loader import getAllFromCategory, getAsset
from src.client.shared import GAMESTATES_TO_BLANDSTRING, GameStates
from src.client.log import log

from random import randint, choice, seed
from time import sleep
from threading import Thread
from math import sin

class AmbienceManager:
    def __init__(self):
        self.songs = getAllFromCategory("songs")
        self.running = True
        self.instance = None
        self.tracks = []

    def update(self, instance):
        """
        AmbienceManager.update() -> AmbienceManager._update() <THREADED>
        """
        log("Initializing Ambience Manager.")
        self.instance = instance
        self.running = True
        instance.spawnNewTask("_update_ambience", self._update)

    async def _update(self, task):
        if self.running == False:
            log("Ambience manager shutting down; self.running is False.", "Worker/Ambience")
            return Task.done
        if self.instance.state == GameStates.END_CREDITS:
            pass
        else:
            if (0 == randint(6, 10) % 2): # 2 in 8 chance
                self.stop_all_tracks()
                song = choice(self.songs)
                if song["conditions"]["playsIn"] == GAMESTATES_TO_BLANDSTRING[self.instance.state]:
                    _song = self.instance.loader.loadSfx(song["path"])
                    _song.play()
                    self.tracks.append(_song)
                    delay = 0
                    if self.instance.state == GameStates.MENU or self.instance.state == GameStates.CONNECTING:
                        delay = randint(70, 150)
                    else:
                        delay = randint(70, 800)
                    log("Sleeping for {} minutes now.".format(delay / 60), "Worker/Ambience")
                    await Task.pause(delay)
                seed(randint(-0x7FFFFF, 0x7FFFFF))
        
        return Task.cont

    def stop_all_tracks(self):
        for song in self.tracks:
            song.stop()

        self.tracks.clear()