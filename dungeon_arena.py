from random import Random
from game import Game
from heroes import Warrior
from player import Player
from randomAgent import RandomAgent
import os

from sarsa import Sarsa
from sarsa_lambda import Sarsa_Lambda

class Arena:
    def __init__(self, players=[]):
        self.players = players
        self.scores = [0 for p in players]

    def addPlayer(self, p):
        self.players.append(p)
        self.scores.append(0)

    def runGame(self):
        g = Game(Warrior(), players=self.players, verbose=False)
        winner = g.run()
        self.scores[winner] += 1

    def run(self, games):
        for i in range(games):
            self.runGame()

        print("Simulated %d games!" % games)
        for i, p in enumerate(self.players):
            print("%s: %d wins" % (p.agent.name(), self.scores[i]))



def main():
    arena = Arena()

    # Add Sarsa Agent
    sa = Sarsa()
    sa.load(
        open(
            os.path.join("example_agents", "Sarsa.pkl"),
            'rb'
        ),
    )
    p1 = Player(sa)
    arena.addPlayer(p1)

    # Add Sarsa Lambda Agent
    sa = Sarsa_Lambda()
    sa.load(
        open(
            os.path.join("example_agents", "Sarsa_Lambda.pkl"),
            'rb'
        ),
    )
    p2 = Player(sa)
    arena.addPlayer(p2)

    # Add Random Agent
    p3 = Player(RandomAgent())
    arena.addPlayer(p3)

    arena.run(100)    

if __name__ == "__main__":
    main()