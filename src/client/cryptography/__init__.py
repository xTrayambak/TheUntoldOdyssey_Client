from cryptography.fernet import Fernet
from random import randint
from sys import maxsize

from base64 import b64encode

from src.log import log, warn

class Cryptography:
    def init():
        log("Initializing AES encryption.", "Worker/CryptoAES")
        _k = str(randint(-maxsize, maxsize))
        key = b64encode(_k.encode("UTF-8"))
        f = open("assets/cache/ENC_KEY", "w") # I don't put this in the resource_locator to make it slightly more difficult to find the key.

        f.write(key.decode("UTF-8"))

        log("Dumped AES encryption key to file.", "Worker/CryptoAES")

        return key

    def encrypt(data):
        key = open("assets/cache/ENC_KEY", "r").read()
        if len(key) < 1:
            log("AES encryption was not able to find a pre-existing key, Cryptography.init has been called instead.", "Worker/CryptoAES")
            key = Cryptography.init()
        
        fernet = Fernet(
            key
        )
        _enc_data = fernet.encrypt(data.encode("UTF-8"))

        log(f"Successfully encrypted data as [{_enc_data}]; success!", "Worker/CryptoAES")

        return _enc_data