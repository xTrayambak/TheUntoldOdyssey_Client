from json import dump, load

PATH = "assets/settings.json"

DATA = load(open(PATH, "r"))

def get_setting(category, name=None, reload: bool = False):
    if reload == True:
        data = load(open(PATH, "r"))

        if name is None:
            return data[category]
 
        return data[category][name]
    else:
        if name is None:
            return DATA[category]

        return DATA[category][name]

def get_all_settings():
    return DATA

def dump_setting(data):
    return dump(obj = data, fp = open(PATH, "w"), indent=4, sort_keys=True)
