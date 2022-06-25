import random
from randomAgent import RandomAgent
from heroes import *
from enum import Enum

class Phase(Enum):
    BIDDING = 0
    DUNGEON = 1

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

class Deck:
    def __init__(self, monsterSet):
        self.cards = []
        for mult, name, strength in monsterSet:
            for i in range(mult):
                self.cards.append(Monster(name, strength))

    def shuffle(self):
        random.shuffle(self.cards)
    
    def isEmpty(self):
        if self.cards:
            return False
        return True

    def draw(self):
        return self.cards.pop()

class PlayerState:
    def __init__(self):
        self.successes = 0
        self.failures = 0
        self.active = True

    def isEliminated(self):
        return self.failures == 2
    
    def isVictorious(self):
        return self.successes == 2

class Player:
    def __init__(self, agent):
        self.agent = agent
        self.state = PlayerState()

    def action(self, obs, actions=None):
        return self.agent.action(obs, actions)

class Game:
    def __init__(self, hero, players=[]):
        self.hero = hero
        self.phase = Phase.BIDDING
        self.deck = Deck(standardMonsters)
        self.deck.shuffle()
        self.dungeon = []
        self.playerNum = len(players)
        self.players = players
        self.currTurn = 0
    
    def __repr__(self):
        return "%d Player Game of Welcome to the Dungeon" % self.playerNum

    def addPlayer(self, player):
        self.playerNum += 1
        self.players.append(player)

    def getObs(self):
        """The game as observed by the current player."""
        return None

    def oneActiveRemains(self):
        counter = 0
        for p in self.players:
            if p.state.active:
                counter += 1
        return counter == 1

    def step(self):
        if self.phase == Phase.BIDDING:
            if self.oneActiveRemains():
                self.phase = Phase.DUNGEON
            else:
                self.biddingStep()
        else:
            pass

    def biddingStep(self):
        currPlayer = self.players[self.currTurn]
        if currPlayer.state.active:
            if self.deck.isEmpty():
                # If the deck is empty the current player must pass
                passes = True
            else:
                passes = currPlayer.action(self.getObs(),[True,False])
            if passes:
                print("Player %d passed!" % self.currTurn)
                currPlayer.state.active = False
            else:
                print("Player %d is still in!" % self.currTurn)
                monster = self.deck.draw()
                a = currPlayer.action(
                    self.getObs(), 
                    self.hero.itemActions + [-1],
                )
                if a == -1:
                    print("Adding a monster to the dungeon")
                    self.dungeon.append(monster)
                else:
                    print("Removing an item")
                    self.hero.remove(a)
            
        self.currTurn = (self.currTurn + 1) % self.playerNum

if __name__=="__main__":
    players = [Player(RandomAgent()) for i in range(3)]
    g = Game(Warrior(), players)
    g.addPlayer(Player(RandomAgent()))
    print(g)
    print(g.deck.cards)
    while g.phase == Phase.BIDDING:
        g.step()
    print(g.hero.items)
    print(g.dungeon)