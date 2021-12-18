#!/usr/bin/env python3
from src.client.loader import getAllFromCategory, getAsset
from src.client.shared import GAMESTATES_TO_STRING, GameStates

from random import randint, choice, seed
from time import sleep
from threading import Thread
from math import sin

class AmbienceManager:
    def __init__(self):
        self.songs = getAllFromCategory("songs")
        self.running = True

    def update(self, instance):
        """
        AmbienceManager.update() -> AmbienceManager._update() <THREADED>
        """
        Thread(target  = self._update, args = (instance, )).start()

    def _update(self, instance):
        sleep(randint(10, 20))
        while self.running == True:
            if instance.state == GameStates.END_CREDITS:
                pass
            else:
                if (2 == randint(5, 10) % 8): # 2 in 8 chance
                    song = choice(self.songs)
                    if song["conditions"]["playsIn"] == GAMESTATES_TO_STRING[instance.state]:
                        instance.loader.loadSfx(song["path"]).play()
                        sleep(randint(100, 250))
                        seed(randint(-0x7FFFFF, 0x7FFFFF))