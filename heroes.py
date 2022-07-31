from equipment import *

class Hero:
    def __init__(self):
        self.maxHP = self.hp
        for item in self.items:
            item.attachToHero(self) 

    def getItemActions(self):
        return list(range(len(self.items)))

    def remove(self, idx):
        self.items.pop(idx)

class Warrior(Hero):
    def __init__(self):
        self.name = "Warrior"
        self.hp = 3
        self.items = [
            PlateArmor(),
            KnightShield(),
            Torch(),
            HolyGrail(),
            VorpalSword(),
            DragonSpear(),
        ]
        Hero.__init__(self)