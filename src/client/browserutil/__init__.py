import webbrowser

class BrowserUtil:
    def __init__(self):
        self.urls = []

    def open(self, url: str = "https://www.google.com"):
        webbrowser.open(url, 1)