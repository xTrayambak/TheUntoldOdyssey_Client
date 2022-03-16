from src.log import *
from src.client.loader import getAsset

narrator_data = getAsset("narrator_dialogs", "en_US")

class NarratorDialogFinder():
    def __init__(self, language: str):
        self.language = language
        
        if language not in narrator_data:
            warn(f"Narrator data for '{language}' could not be found!", "Worker/NarratorDialog")
            self.data = {}
        else:
            self.data = narrator_data[language]

    def set_language(self, language: str):
        log("Refreshing narrator data.", "Worker/NarratorDialog")
        if language not in narrator_data:
            warn(f"Narrator data for '{language}' could not be found!", "Worker/NarratorDialog")
            self.language = language
            self.data = {}
        else:
            self.language = language
            self.data = narrator_data[language]
        
    def get_dialog(self, tag: str):
        if tag in self.data:
            return self.data[tag]
        else:
            warn(f"No narrator data found in language '{self.language}' for narrator tag '{tag}'", "Worker/NarratorDialog")
            return f"error, no narrator data found for narrator tag [{tag}]"