#!/usr/bin/env python3
from direct.task import Task
from random import randint, choices

from src.client.loader import getAllFromCategory, getAsset
from src.client.shared import GAMESTATES_TO_BLANDSTRING, GameStates
from src.log import log, warn

"""
SONG LIST:
song001: Y&YG - Gone [INGAME]
song002: Y&YG - Harbinger of Joy [INGAME]
song003: Y&YG - Unlighted [MENU]
song004: Y&YG - White Phantom [CREDITS]
song005: WORMSWORTH - Sonata #1 [INGAME]
song006: WORMSWORTH - Mist #1 [VOIDLANDS]
song007: WORMSWORTH - Mist #2 [VOIDLANDS]
"""

probability_ingame_overworld = {
    'night':[5.5, 0.1, 0.02],
    'day': [0.02, 5.5, 5.7],
    'evening': [0.9, 0.1, 0.00001],
    'early_day': [0.9, 1.2, 1.2]
}

probability_ingame_hell = {
    'night': [0.0, 0.0, 0.0],
    'day': [0.0, 0.0, 0.0],
    'evening': [0.0, 0.0, 0.0],
    'early_day': [0.0, 0.0, 0.0]
}

probability_ingame_voidlands = {
    'night': [2.3, 3.4],
    'day': [3.4, 2.3],
    'evening': [2.3, 3.4],
    'early_day': [4.5, 4.4]
}

probability_menu = [4.34]

songs_menu = ['assets/music/unlighted.mp3']

songs_ingame_overworld = ['assets/music/gone.mp3', 'assets/music/harbinger_of_joy.mp3', 'assets/music/sonata.flac']
songs_ingame_hell = []
songs_ingame_voidlands = ['assets/music/mist001.flac', 'assets/music/mist002.flac']

class AmbienceManager:
    def __init__(self, instance):
        self.songs = getAllFromCategory('songs')
        self.running = True
        self.instance = None
        self.tracks = []

        self.instance = instance

        self.running = True
        self.end_credits = self.instance.audioLoader.load('assets/music/white_phantom.mp3')
        self.end_credits_playing = False

        self.tracks.append(self.end_credits)

    async def _update(self, task):
        tuo = self.instance
        
        # Initial delay before the main menu loads up.
        #await Task.pause(randint(10, 25))
        
        if self.running == False:
            log("Ambience manager shutting down; self.running is False.", "Worker/Ambience")
            return Task.done
            
        if tuo.getState() == GameStates.END_CREDITS:
            if self.end_credits.status() == self.end_credits.READY:
                self.endCreditsPlaying = True

                self.end_credits.play()
                self.end_credits.set_loop(True)
        elif tuo.getState() == GameStates.MENU or tuo.getState() == GameStates.CONNECTING:
            song = tuo.audioLoader.load(choices(population=songs_menu, weights=probability_menu)[0])
            song.play()

            await Task.pause(
                randint(int(song.get_length()), int(70+song.get_length()))
            )
        elif tuo.getState() == GameStates.INGAME:
            if tuo.game.get_dimension() == tuo.getSharedData().DIMENSION.OVERWORLD:
                song = tuo.audioLoader.load(choices(population=songs_ingame_overworld, weights=probability_ingame_overworld))

                await Task.pause(
                    randint(int(song.get_length()), int(100+song.get_length()))
                )
            elif tuo.game.get_dimension() == tuo.getSharedData().DIMENSION.VOIDLANDS:
                song = tuo.audioLoader.load(choices(population=songs_ingame_voidlands, weights=probability_ingame_voidlands))
                song.play()

        return Task.cont

    def stop_all_tracks(self):
        for song in self.tracks:
            song.stop()

        self.tracks.clear()
