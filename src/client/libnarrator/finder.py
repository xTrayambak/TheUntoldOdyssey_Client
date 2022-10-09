import json

from src.log import *
from src.client.loader import getAsset

class NarratorDialogFinder:
    def __init__(self, language: str):
        self.language = language
        narrator_data = getAsset("narrator_dialogs", language)

        if language not in narrator_data:
            warn(f"Narrator data for '{language}' could not be found!", "Worker/NarratorDialog")
            self.data = {}
        else:
            log(narrator_data, "NARRATORDATA")
            self.data = json.load(fp=open(narrator_data, "r"))

    def set_language(self, language: str):
        log("Refreshing narrator data.", "Worker/NarratorDialog")
        narrator_data = getAsset("narrator_dialogs", language)
        if language not in narrator_data:
            warn(f"Narrator data for '{language}' could not be found!", "Worker/NarratorDialog")
            self.language = language
            self.data = {}
        else:
            self.language = language
            self.data = json.load(fp=open(narrator_data, "r"))

    def get_dialog(self, tag: str):
        if tag in self.data:
            return self.data[tag]
        else:
            warn(f"No narrator data found in language '{self.language}' for narrator tag '{tag}'", "Worker/NarratorDialog")
            return f"error, no narrator data found for narrator tag [{tag}]"
