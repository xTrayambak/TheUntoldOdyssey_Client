import pickle

def decode(string):
    return pickle.loads(string)

def encode(data) -> bytes:
    return pickle.dumps(data)