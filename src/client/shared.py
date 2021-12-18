#!/usr/bin/env python3
from enum import Enum

from src.client.state_execution import *

class GameStates(Enum):
    LOADING = 0
    MENU = 1
    SETTINGS = 2
    INGAME = 3
    END_CREDITS = 4,
    CONNECTING = 5


GAMESTATES_TO_STRING = {
    GameStates.LOADING: "loading",
    GameStates.MENU: "menu",
    GameStates.SETTINGS: "settings",
    GameStates.INGAME: "ingame",
    GameStates.END_CREDITS: "end_credits",
    GameStates.CONNECTING: "connecting_to_server"
}

GAMESTATE_TO_FUNC = {
    GameStates.LOADING: loadingScreen,
    GameStates.MENU: mainMenu,
    GameStates.END_CREDITS: endCredits,
    GameStates.INGAME: inGameState,
    GameStates.CONNECTING: connectingPage
}