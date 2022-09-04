import pyttsx3
from multiprocessing.pool import ThreadPool

from src.client.settingsreader import get_setting
from src.log import *


class NarratorUtil:
    def __init__(self, instance):
        self.engine = None
        self.instance = instance
 
        try:
            self.engine = pyttsx3.init()
        except Exception as exc:
            warn(f"UNABLE TO INITIALIZE TEXT2SPEECH ENGINE! [{exc}]")

        self.pool = ThreadPool(4)

        self.enabled = get_setting("accessibility", "narrator")

        if self.enabled:
            log("Narrator is enabled.")
        else:
            log("Narrator is disabled.")

    def refresh(self):
        if self.engine is None: return
        self.enabled = get_Setting("accessibility", "narrator")

        if self.enabled:
            log("Narrator is enabled.")
        else:
            log("Narrator is disabled.")


    def say(self, text: str = "Hello, World!") -> bool:
        """
        <THREADED>Query the narration engine to say a sentence.
        """
        if self.enabled != True: return self.enabled

        self.pool.apply_async(self._say, (self.instance.narrator_dialog_finder.get_dialog(text)))

        return True

    def _say(self, text: str = "Hello, World!") -> int:
        """
        Query the narration engine to say a sentence.
        """
        self.engine.say(text)
        self.engine.runAndWait()

        return 1

    def stop(self) -> int:
        """
        Stop the narration engine.
        """
        self.engine.stop()
        return 1
