import webbrowser

class BrowserUtil:
    def __init__(self):
        self.urls = []

    def goto(self, url: str = "https://www.google.com"):
        webbrowser.open(url, 1)