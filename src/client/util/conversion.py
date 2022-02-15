def encodedToDecoded(string:str) -> dict:
    splits = string.split("|")
    message_type = splits[0]

    return {'type': message_type, 'extra': splits[1]}

def encode(message_type: str, data: any) -> str:
    return "{}|{}".format(message_type, data)