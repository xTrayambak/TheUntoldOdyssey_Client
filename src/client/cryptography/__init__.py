## [!] WORK IN PROGRESS, DO NOT USE
## MIGHT BE USED IN FUTURE VERSIONS.

## FINDING AN ALTERNATIVE TO PYCRYPTO AS PYCRYPTO HAS A RCE VULNERABILITY DUE TO AN OVERFLOW EXPLOIT!
from os import urandom

"""
Decryption: Unpad
"""
def unpad(s): 
    return s.rstrip()

"""
Decryption: Pad

(AES256 needs 16 byte blocks)
"""
def pad(string: str):
    remainder = len(string) % 16
    padding_needed = 16 - remainder
    return string + padding_needed * ' '

