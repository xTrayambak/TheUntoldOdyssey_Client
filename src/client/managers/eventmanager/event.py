class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.triggered = False
        self.hooks = []

    def hook(self, function):
        self.hooks.append(function)

    def call_all(self):
        for func in self.hooks:
            func()

    def trigger(self):
        self.triggered = True
        self.call_all()

    def reset(self):
        self.triggered = False