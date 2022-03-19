from pickle import dumps, loads

def encode_object(obj) -> bytes:
    return dumps(obj)

def decode_object(obj):
    return loads(obj)