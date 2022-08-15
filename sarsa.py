from agent import Agent
from copy import deepcopy
import random
import pickle
from bridge import minimal_bridge

class Sarsa(Agent):
    def __init__(self, learning = True, alpha=0.4, eps=0.1):
        self.Q = dict()
        self.learning = learning
        self.alpha = alpha
        self.eps = eps
        self.s_last = None
        self.a_last = None
        self.bridge = lambda x: minimal_bridge(self, x)
    
    def action(self, obs, actions, description=None):
        s, R = self.bridge(obs)

        #s = str(s)

        #s = (s['dungeonSize'], str(s['monsterDrawn']), s['currItemCode'])

        maxVal = -float('inf')
        chosenA = None
        for a in actions:
            if not (s,a) in self.Q:
                self.Q[(s,a)] = 1
            if self.Q[(s,a)] > maxVal:
                maxVal = self.Q[(s,a)]
                chosenA = a

        if random.random() < self.eps:
            chosenA = random.choice(actions)

        #print("In state " + str(s) + " choosing action " + str(chosenA))
        if self.learning and not self.s_last is None:
            self.Q[(self.s_last, self.a_last)] += self.alpha * (
                R + 1 * self.Q[(s,chosenA)] - self.Q[(self.s_last, self.a_last)]
            )
        self.s_last, self.a_last = s, chosenA
        return chosenA

    def save(self, f):
        pickle.dump(self.Q, f)

    def load(self, f):
        self.Q = pickle.load(f)

    def terminateEpisode(self, win=False):
        if win == True:
            R = 1
        else:
            R = 0

        self.Q[(self.s_last, self.a_last)] += self.alpha * (
                R + 1 * 0 - self.Q[(self.s_last, self.a_last)]
        )

        self.s_last, self.a_last = None, None

if __name__ == "__main__":
    a = Sarsa()
    f = open("Q.pkl", 'wb')
    a.save(f)
    a.load(f)
