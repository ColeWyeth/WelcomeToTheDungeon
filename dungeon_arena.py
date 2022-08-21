from random import Random
from game import Game
from heroes import Warrior
from player import Player
from randomAgent import RandomAgent
import os

from sarsa import Sarsa
from sarsa_lambda import Sarsa_Lambda

class Arena:
    def __init__(self, agents=[]):
        self.agents = agents
        self.scores = [0 for p in self.agents]

    def addAgent(self, a):
        self.agents.append(a)
        self.scores.append(0)

    def runGame(self):
        g = Game(Warrior(), players=[Player(a) for a in self.agents], verbose=False)
        winner = g.run()
        self.scores[winner] += 1
        for i, a in enumerate(self.agents):
            a.terminateEpisode(winner == i)

    def run(self, games):
        for i in range(games):
            self.runGame()

        print("Simulated %d games!" % games)
        for i, a in enumerate(self.agents):
            print("%s: %d wins" % (a.name(), self.scores[i]))



def main():
    arena = Arena()

    # # Add Sarsa Agent
    # sa = Sarsa()
    # sa.load(
    #     open(
    #         os.path.join("example_agents", "Sarsa.pkl"),
    #         'rb'
    #     ),
    # )
    # arena.addAgent(sa)

    # Add Sarsa Agent (recursive training)
    sa = Sarsa()
    sa.load(
        open(
            os.path.join("example_agents", "Sarsa_rec.pkl"),
            'rb'
        ),
    )
    arena.addAgent(sa)

    # # Add Sarsa Lambda Agent
    # sla = Sarsa_Lambda()
    # sla.load(
    #     open(
    #         os.path.join("example_agents", "Sarsa_Lambda.pkl"),
    #         'rb'
    #     ),
    # )
    # arena.addAgent(sla)

    # Add Sarsa Lambda Agent (recursive training)
    sla = Sarsa_Lambda()
    sla.load(
        open(
            os.path.join("example_agents", "Sarsa_Lambda_rec.pkl"),
            'rb'
        ),
    )
    arena.addAgent(sla)

    # Add Random Agent
    ra = RandomAgent()
    arena.addAgent(ra)

    arena.run(100)    

if __name__ == "__main__":
    main()