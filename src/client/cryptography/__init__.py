import os
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

from src.log import log, warn

class Cryptography:
    '''
    I forgor cryptography.
    '''
    def __init__(self, key: str):
        self.key = key
        self.fernet = Fernet(key)
    
    def encrypt(self, data):
        self.fernet.encrypt()
