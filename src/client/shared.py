#!/usr/bin/env python3
"""
Contains the data that is going to be shared amongst multiple client scripts so circular imports don't happen.
"""
from enum import IntEnum, Enum

from src.client.states.connectingscreen import connectingPage
from src.client.states.creditsroll import endCredits
from src.client.states.debug_state import debug_state
from src.client.states.ingame import inGameState
from src.client.states.mainmenu import mainMenu
from src.client.states.settings import settingsPage


class GameStates(IntEnum, Enum):
    LOADING = 0
    MENU = 1
    SETTINGS = 2
    INGAME = 3
    END_CREDITS = 4,
    CONNECTING = 5,
    DEBUG = 6

class TextFormatting:
    JUMBLE = "[J]"
    UNDERLINE = "[U]"

GAMESTATES_TO_BLANDSTRING = {
    GameStates.LOADING: "loading",
    GameStates.MENU: "menu",
    GameStates.SETTINGS: "settings",
    GameStates.INGAME: "ingame",
    GameStates.END_CREDITS: "end_credits",
    GameStates.CONNECTING: "connecting",
    GameStates.DEBUG: "debug"
}

GAMESTATES_TO_STRING = {
    GameStates.LOADING: "On the Loading Screen",
    GameStates.MENU: "On the Menu",
    GameStates.SETTINGS: "In the Settings Menu",
    GameStates.INGAME: "In-Game",
    GameStates.END_CREDITS: "Watching the End Credits",
    GameStates.CONNECTING: "Connecting to The Server",
    GameStates.DEBUG: "Are ya coding son?"
}

GAMESTATE_TO_FUNC = {
    GameStates.MENU: mainMenu,
    GameStates.END_CREDITS: endCredits,
    GameStates.INGAME: inGameState,
    GameStates.CONNECTING: connectingPage,
    GameStates.SETTINGS: settingsPage,
    GameStates.DEBUG: debug_state
}

class Language:
    ENGLISH = "english"
    HINDI = "hindi"
    THAI = "thai"
    BAHASAINDONESIA = "bahasaindonesia"
    MALAY = "malay"

DisconnectStatusCodes = {
    "disconnect-server_shutdown": "The server has shut down and is currently restarting.",
    "disconnect-admin_kick": "You were kicked by a server admin!",
    "disconnect-anticheat": "Proximity Anticheat has detected that your client behaviour is suspicious! If this is a false report, please contact Syntax Studios.",
    "disconnect-high_ping": "Your ping is very high! We have had to disconnect you.",
    "disconnect-auth_fail": "Invalid Syntax Studios account credentials (Try restarting the game)",
    "disconnect-login_from_other_location": "Your account was logged in from another location.\nRelaunch the game and the launcher.",
    "disconnect-kicknoreason": "You were disconnected!",
    "disconnect-outdatedversion": "Your version of the client is outdated! (Install the latest update)",
    "disconnect-unabletoconnect": "Unable to connect to the servers.\nContact Syntax Studios if the problem persists.",
    "disconnect-timeout": "Timed out.\nPlease check your internet connection.",
    "disconnect-throttled": "Connection throttled!\nPlease wait before joining."
}

DATA_PROVIDER = "https://tuoDataDelivery.xtrayambak.repl.co/"
SYNTAX_PAYMENTS_PROVIDER = "https://syntaxpayments.xtrayambak.repl.co/"
SYNTAX_AUTHENTICATION_PROVIDER = "https://waveauthserver.pythonanywhere.com/"