from json import dump, load

PATH = "assets/settings.json"

DATA = load(open(PATH, "r"))

def getSetting(category, name):
    return DATA[category][name]