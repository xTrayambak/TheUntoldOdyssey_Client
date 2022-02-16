import pyttsx3

from multiprocessing.pool import ThreadPool

from src.log import *
from src.client.settingsreader import getSetting

class NarratorUtil:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.pool = ThreadPool(4)

        self.enabled = getSetting("accessibility", "narrator")

        if self.enabled:
            log("Narrator is enabled.")
        else:
            log("Narrator is disabled.")

    def refresh(self):
        self.enabled = getSetting("accessibility", "narrator")

        if self.enabled:
            log("Narrator is enabled.")
        else:
            log("Narrator is disabled.")


    def say(self, text: str = "Hello, World!") -> bool:
        """
        <THREADED>Query the narration engine to say a sentence.
        """
        if self.enabled != True: return self.enabled

        self.pool.apply_async(self._say, (text,))

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