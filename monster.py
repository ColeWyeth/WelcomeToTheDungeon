from enum import Enum

class MS(Enum):
    GOBLIN = 1
    SKELETON = 2
    ORC = 3
    VAMPIRE = 4
    GOLEM = 5
    LICH = 6
    DEMON = 7
    DRAGON = 9

class Monster:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

    def __repr__(self):
        return "%s: %d" % (self.name, self.strength)

standardMonsters = set([
    (2, "Goblin", MS.GOBLIN.value),
    (2, "Skeleton", MS.SKELETON.value),
    (2, "Orc", MS.ORC.value),
    (2, "Vampire", MS.VAMPIRE.value),
    (2, "Golem", MS.GOLEM.value),
    (1, "Lich", MS.LICH.value),
    (1, "Demon", MS.DEMON.value),
    (1, "Dragon", MS.DRAGON.value),
])