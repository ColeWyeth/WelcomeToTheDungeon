class Equipment:
    def __init__(self, name):
        self.name = name

class Hero:
    def __init__(self):
        self.name = "Example"
        self.initHealth(0)
        self.items = []
        self.setItemActions()

    def initHealth(self, value):
        self.startinHealth = value
        self.health = value

    def setItemActions(self):
        self.itemActions = list(range(len(self.items)))

    def remove(self, idx):
        self.items.pop(idx)
        self.setItemActions()

class Warrior(Hero):
    def __init__(self):
        self.name = "Warrior"
        self.initHealth(3)
        self.items = [
            Equipment("Vorpal Sword"),
            Equipment("Shield"), # TODO: make these accurate
        ]
        self.setItemActions()
