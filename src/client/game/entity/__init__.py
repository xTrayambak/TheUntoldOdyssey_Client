class Entity:
    def __init__(self, name: str, position: list = [0, 0, 0]):
        self.name = name
        self.position = position

    def setPos(self, position: list):
        self.position = position