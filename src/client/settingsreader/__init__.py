from json import dump, load

PATH = "assets/settings.json"

DATA = load(open(PATH, "r"))

def getSetting(category, name=None):
    if name is None:
        return DATA[category]
        
    return DATA[category][name]

def getAllSettings():
    return DATA

def dumpSetting(data):
    return dump(obj = data, fp = open(PATH, "w"))