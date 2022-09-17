import json
import os
from unittest.util import strclass

from src.log import *

TRANSLATION_PATH = "assets/translations/"

class TranslationUtility:
    def __init__(self, language: str = "english"):
        if os.path.exists(TRANSLATION_PATH + language + ".json") != True:
            warn(f"Translation files for language [{TRANSLATION_PATH}{language}.json] do NOT exist! Translations will just default to their own.", "Worker/TranslationUtil")
            self.translations = {}
        else:
            log(f"Loading translations for language [{language}]")
            self.language = language.lower()

            self.translations = json.load(
                open(TRANSLATION_PATH + language + ".json", "r", encoding = 'utf-8')
            )

    def update(self, language: str):
        """
        Re-load the translation files.
        """
        self.language = language.lower()

        self.translations = json.load(
            open(TRANSLATION_PATH + language + ".json", "r", encoding = 'utf-8')
        )

    def translate(self, string_text: str):
        """
        Translate something from category and text. 
        """
        if string_text not in self.translations:
            return string_text

        return self.translations[string_text]
