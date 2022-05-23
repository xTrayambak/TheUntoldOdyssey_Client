#!/usr/bin/env python3
from direct.task import Task
from src.client.loader import getAllFromCategory, getAsset
from src.client.shared import GAMESTATES_TO_BLANDSTRING, GameStates
from src.log import log, warn

from random import randint, choices

"""
SONG LIST:
song001: Y&YG - Gone [INGAME]
song002: Y&YG - Harbinger of Joy [INGAME]
song003: Y&YG - Unlighted [MENU]
song004: Y&YG - White Phantom [CREDITS]
song005: WORMSWORTH - Sonata #1 [INGAME]
song006: WORMSWORTH - Mist #1 [MENU]
song007: WORMSWORTH - Mist #2 [MENU]
"""

probability_ingame = {
    'night':[5.5, 0.1, 0.02],
    'day': [0.02, 5.5, 5.7],
    'evening': [0.9, 0.1, 0.00001],
    'early_day': [0.9, 1.2, 1.2]
}

probability_menu = [4.34, 4.3, 2.5]

songs_menu = ['song003', 'song006', 'song007']
songs_ingame = ['song001', 'song002', 'song005']

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
        self.end_credits = self.instance.loader.loadSfx("assets/music/white_phantom.mp3")
        self.endCreditsPlaying = False
        self.tracks.append(self.end_credits)
        instance.spawnNewTask("_update_ambience", self._update)

    async def _update(self, task):
        tuo = self.instance

        await Task.pause(randint(10, 25))
        
        if self.running == False:
            log("Ambience manager shutting down; self.running is False.", "Worker/Ambience")
            return Task.done
            
        if tuo.getState() == GameStates.END_CREDITS:
            if self.end_credits.status() == self.end_credits.READY:
                self.endCreditsPlaying = True

                self.end_credits.play()
                self.end_credits.setLoop(True)
        elif tuo.getState() == GameStates.MENU or tuo.getState() == GameStates.CONNECTING:
            song = tuo.audioLoader.load(0, choices(population=songs_menu, weights=probability_menu)[0])
            song.play()

            await Task.pause(
                randint(int(song.length()), int(70+song.length()))
            )
        elif tuo.getState() == GameStates.INGAME:
            song = tuo.audioLoader.load(0, choices(population=songs_ingame, weights=probability_menu))

            await Task.pause(
                randint(int(song.length()), int(100+song.length()))
            )

        return Task.cont

    def stop_all_tracks(self):
        for song in self.tracks:
            song.stop()

        self.tracks.clear()