#!/usr/bin/env python3
from enum import IntEnum, Enum

from src.client.state_execution import *

class GameStates(IntEnum, Enum):
    LOADING = 0
    MENU = 1
    SETTINGS = 2
    INGAME = 3
    END_CREDITS = 4,
    CONNECTING = 5


GAMESTATES_TO_BLANDSTRING = {
    GameStates.LOADING: "loading",
    GameStates.MENU: "menu",
    GameStates.SETTINGS: "settings",
    GameStates.INGAME: "ingame",
    GameStates.END_CREDITS: "end_credits",
    GameStates.CONNECTING: "connecting"
}

GAMESTATES_TO_STRING = {
    GameStates.LOADING: "On the Loading Screen",
    GameStates.MENU: "On the Menu",
    GameStates.SETTINGS: "In the Settings Menu",
    GameStates.INGAME: "In-Game",
    GameStates.END_CREDITS: "Watching the End Credits",
    GameStates.CONNECTING: "Connecting to The Server"
}

GAMESTATE_TO_FUNC = {
    GameStates.LOADING: loadingScreen,
    GameStates.MENU: mainMenu,
    GameStates.END_CREDITS: endCredits,
    GameStates.INGAME: inGameState,
    GameStates.CONNECTING: connectingPage
}