import os
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

#from src.log import log, warn

def pad_missing_bytes(data: bytes):
    data = data.decode('utf-8')

    for i in range(32 - len(data)):
        data += ' '

    return data.encode('utf-8')


def fmt_key(key: bytes) -> bytes:
    b64_padded_key = pad_missing_bytes(key)

    return urlsafe_b64encode(b64_padded_key)


class Cryptography:
    '''
    Cryptography module.
    '''
    def __init__(self, key: str):
        self.key = fmt_key(key.encode('utf-8'))
        self.fernet = Fernet(self.key)

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt(self, data: bytes):
        return self.fernet.decrypt(data)
