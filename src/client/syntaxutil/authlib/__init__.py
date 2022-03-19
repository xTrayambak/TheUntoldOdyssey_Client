from src.log import *
from src.client.syntaxutil.authlib.session import Session

class Authenticator:
    def __init__(self, instance):
        self.instance = instance
        self.session = None

    def get_auth_server_status(self):
        return Session().get_auth_server_status()

    def start_auth(self):
        log("Authenticator is starting auth process...", "Worker/Authenticator")

        """self.session = Session()
        try:
            self.session.authenticate(self.instance, self.instance.token)
        except Exception as e:
            warn(f"Authentication failed: [{e}]")"""

        log("Authenticator has completed it's auth process...", "Worker/Authenticator")