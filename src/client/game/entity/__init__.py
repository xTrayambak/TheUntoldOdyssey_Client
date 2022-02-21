class Entity:
    def __init__(self, name: str, position: list | tuple = [0, 0, 0]):
        self.name = name
        self.position = position

    def setPos(self, position: list | tuple):
        self.position = position