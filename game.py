import random
from randomAgent import RandomAgent
from terminalAgent import TerminalAgent
from equipment import EffectCode
from heroes import *
from monster import Monster, standardMonsters, MS
from player import Player
from enum import Enum

class Phase(Enum):
    BIDDING = 0
    DUNGEON = 1

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
        self.monsterDrawn = None
    
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
        activePlayerTurn = None
        for i, p in enumerate(self.players):
            if p.isActive():
                counter += 1
                activePlayerTurn = i
        return (counter == 1, activePlayerTurn)

    def step(self):
        if self.phase == Phase.BIDDING:
            exactlyOneActive, activePlayerTurn = self.oneActiveRemains()
            if exactlyOneActive:
                self.currTurn = activePlayerTurn
                self.phase = Phase.DUNGEON
                self.runDungeonSetup()
                assert self.players[self.currTurn].isActive()
            else:
                self.biddingStep()
        else:
            if self.hero.hp <= 0:
                print("The hero has died!")
                self.players[self.currTurn].takeLoss() 
                self.runBiddingSetup()
            elif not self.dungeon:
                print("Dungeon clear!")
                self.players[self.currTurn].takeWin()
                self.runBiddingSetup()
            else:
                self.dungeonStep()

    def checkForWinner(self):
        numEliminated = 0
        playerTurnNotEliminated = None
        for i, p in enumerate(self.players):
            if p.state.isVictorious():
                return i
            if p.state.isEliminated():
                numEliminated += 1
            else:
                playerTurnNotEliminated = i
        if numEliminated == len(players) - 1:
            return playerTurnNotEliminated
        else:
            return None 

    def runBiddingSetup(self):
        print("Bidding Phase Beginning!")
        self.phase = Phase.BIDDING
        for p in self.players:
            p.state.active = not p.state.isEliminated()
        self.hero = Warrior() # TODO: Appropriate type
        self.deck = Deck(standardMonsters)
        self.deck.shuffle()

    def biddingStep(self):
        currPlayer = self.players[self.currTurn]
        if currPlayer.state.active:
            if self.deck.isEmpty():
                # If the deck is empty the current player must pass
                passes = True
            else:
                passes = currPlayer.action(
                    self.getObs(),[True,False],"Will you pass (0/1)? "
                )
            if passes:
                print("Player %d passed!" % self.currTurn)
                currPlayer.state.active = False
            else:
                print("Player %d is still in!" % self.currTurn)
                prompt = "Current items: " + str(self.hero.items) + "\n"
                prompt += "Remove one using its index (from 0).\n"
                prompt += "Enter -1 to add the monster to the dungeon! "
                monster = self.deck.draw()
                self.monsterDrawn = monster
                a = currPlayer.action(
                    self.getObs(), 
                    self.hero.getItemActions() + [-1],
                    prompt,
                )
                if a == -1:
                    print("Adding a monster to the dungeon")
                    self.dungeon.append(monster)
                else:
                    print("Removing an item: %s" % self.hero.items[a])
                    self.hero.remove(a)
                self.monsterDrawn = None
            
        self.currTurn = (self.currTurn + 1) % self.playerNum

    def runDungeonSetup(self):
        print("Dungeon Phase Beginning!")
        #print("Dungeon: " + str(self.dungeon))
        print("There are %d monsters in this dungeon!" % len(self.dungeon))
        print("Items: " + str(self.hero.items))
        for item in self.hero.items:
            code = item.runPreEntry()
            if code is None:
                continue
            else:
                self.handleSetupCode(item, code)

    def handleSetupCode(self, item, code):
        if code == EffectCode.VORPAL:
            prompt = "Which monster would you like to defeat automatically? "
            prompt += "(Enter its strength): "
            msv = self.players[self.currTurn].action(
                self.getObs(),
                [ms.value for ms in MS],
                prompt,
            )
            item.setTarget(msv)  
            print(
                "Player %d is prepared to kill strength %d monsters using %s" %
                (self.currTurn, msv, item.name)
            )

    def dungeonStep(self):
        m = self.dungeon.pop()
        print("Player %d drew a %s" % (self.currTurn, m.name))
        for item in self.hero.items:
            if m.strength in item.getAutoTargets():
                print("%s killed by %s" % (m.name, item.name))
                return
        for item in self.hero.items:
            optionalTargets = item.getOptionalTargets()
            if optionalTargets is None:
                continue
            if m.strength in optionalTargets:
                pass # TODO: this is irrelevant for Warrior but important

        # The monster is not defeated by any item
        self.hero.hp -= m.strength

    def getObs(self):
        return self.monsterDrawn # TODO: Make this an actual state

if __name__=="__main__":
    players = [Player(RandomAgent()) for i in range(6)]
    g = Game(Warrior(), players)
    g.addPlayer(Player(TerminalAgent()))
    print(g)
    #print(g.deck.cards)
    while True:
        winner = g.checkForWinner()
        if not winner is None:
            print("Player %d won!" % winner)
            break
        g.step()