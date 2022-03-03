import requests
import hashlib

from src.client.shared import DATA_PROVIDER
from src.log import *

hasher = hashlib.md5()

class Session:
    def __init__(self):
        self.requests = []
        self.authenticated = False

    def authenticate(self, instance, token: str = ""):
        log("Asking server to start session.", "Worker/SyntaxAuthLib")
        start_flag = requests.get(
            DATA_PROVIDER + "api/v2/session/instantiate"
        ).json()

        if start_flag['result'] == True:
            log("Server has let us open a session!", "Worker/SyntaxAuthLib")
        else:
            warn("Server has declined the authentication request.", "Worker/SyntaxAuthLib")
            instance.warn(
                f"Syntax Studios Authentication Failed",
                "We tried connecting to our servers and the server declined.",
                "Okay", "Quit"
            )
        
        hasher.update(instance.version.encode("utf-8"))
        client_hash = f"{hasher.hexdigest()}_VANILLA"
        
        log(f"Client hash is {client_hash}, asking server to verify.", "Worker/SyntaxAuthLib")