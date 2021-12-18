class GameObject:
    def __init__(self, name, workspace):
        self.parent = None
        self.children = {}

        self.workspace.add_object(name, self)

    def add_child(self, name, obj):
        self.children.update({name: obj})