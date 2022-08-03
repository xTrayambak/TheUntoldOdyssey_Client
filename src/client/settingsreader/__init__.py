from json import dump, load

PATH = "assets/settings.json"

DATA = load(open(PATH, "r"))

def getSetting(category, name=None, reload: bool = False):
    if reload == True:
        data = load(open(PATH, "r"))

        if name is None:
            return data[category]
            
        return data[category][name]
    else:
        if name is None:
            return DATA[category]
            
        return DATA[category][name]

def getAllSettings():
    return DATA

def dumpSetting(data):
    # this will help!
    return dump(obj = data, fp = open(PATH, "w"), indent=4, sort_keys=True)