from enum import Enum

class EffectCode(Enum):
    VORPAL = 0


class Equipment:
    def __init__(self, name):
        self.name = name
        self.hero = None

    def attachToHero(self, hero):
        self.hero = hero

    def getAutoTargets(self):
        """
        Many items automatically kill certain monsters. This will not require 
        a choice (there does not appear to be any situation in which a player
        would reasonably prefer not to use such an effect). 
        """
        return set()

    def getOptionalTargets(self):
        """
        Many items can be used at a player's discretion during the dungeon
        phase on certain targets. When this is the case, it will be handled by
        the getDungeonEffectCode function.
        """

    def runPreEntry(self):
        """
        Some items have effects on the game state when used before the dungeon
        phase. Such effects are best handled in the game loop. By default, 
        return None for no effect. Otherwise return an EffectCode.
        Any effects local to the attached hero take place in this function.
        """
        return None

    def getDungeonEffectCode(self):
        """
        Some items have effects on the game state when used during the dungeon
        phase. Such effects are best handled in the game loop. By default, 
        return None for no effect. Otherwise return an EffectCode. 
        """
        return None

class PlateArmor(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Plate Armor")

    def runPreEntry(self):
        if self.hero is None:
            raise Exception("Equipment is not attached to a hero!")
        else:
            self.hero.hp += 5
    return Equipment.runPreEntry(self)

class KnightShield(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Knight Shield")

    def runPreEntry(self):
        if self.hero is None:
            raise Exception("Equipment is not attached to a hero!")
        else:
            self.hero.hp += 3
    return Equipment.runPreEntry(self)

class Torch(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Torch")

    def getAutoTargets(self):
        return set([1,2,3])

class HolyGrail(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Holy Grail")
    
    def getAutoTargets(self):
        return set([2,4,6])

class VorpalSword(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Vorpal Sword")

    def runPreEntry(self):
        return EffectCode.VORPAL

    def setTarget(self, target):
        """
        The game loop must call this while handling the VORPAL EffectCode.
        """
        self.target = target

    def getAutoTargets(self):
        return set([target])

class DragonSpear(Equipment):
    def __init__(self):
        Equipment.__init__(self, "Dragon Spear")

    def getAutoTargets(self):
        return set([9])