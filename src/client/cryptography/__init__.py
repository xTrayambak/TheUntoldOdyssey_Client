from cryptography.fernet import Fernet
from random import randint
from sys import maxsize

from src.client.log import log

class Cryptography:
    def init():
        log("Initializing AES encryption.", "Worker/CryptoAES")
        key = randint(-maxsize, maxsize)
        f = open("assets/cache/ENC_KEY", "w") # I don't put this in the resource_locator to make it slightly more difficult to find the key.

        f.write(key)

        log("Dumped AES encryption key to file.", "Worker/CryptoAES")

        return key

    def encrypt(data):
        key = open("assets/cache/ENC_KEY", "r").read()
        if len(key) > 1:
            log("AES encryption was not able to find a pre-existing key, Cryptography.init has been called instead.", "Worker/CryptoAES")
            key = Cryptography.init()
        
        fernet = Fernet(bytes(key))
        _enc_data = fernet.encrypt(bytes(data))

        log(f"Successfully encrypted data as [{_enc_data}]; success!", "Worker/CryptoAES")

        return _enc_data