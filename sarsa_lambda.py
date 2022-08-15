from agent import Agent
from copy import deepcopy
import random
import pickle
from bridge import minimal_bridge

# Page 305 of Sutton and Barto
class Sarsa_Lambda(Agent):
    def __init__(self, learning = True, alpha=0.1, eps=0.1, lmbda = 0.5):
        self.Q = dict()
        self.z = dict()
        self.delta = 0
        self.learning = learning
        self.alpha = alpha
        self.eps = eps
        self.lmbda = lmbda
        self.s_last = None
        self.a_last = None
        self.bridge = lambda x: minimal_bridge(self, x)

    def acc_z(self, z, s, a):
        if (s, a) not in z.keys():
            z[(s, a)] = 0
        z[(s,a)] += 1
    
    def action(self, obs, actions, description=None):
        s, R = self.bridge(obs)

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
            # Here s_last,a_last act as S,A
            self.delta = R - self.Q[(self.s_last,self.a_last)] # R - w_i (R is always 0 for WTTD)
            self.acc_z(self.z, self.s_last, self.a_last) # accumulating traces

            # Here s,a act as S',A'
            self.delta += self.Q[(s,a)]
            for k in self.z.keys(): # all activated states
                # TODO: multiple by gamma where appropriate
                self.Q[k] += self.alpha*self.delta*self.z[k]
                self.z[k] = self.lmbda*self.z[k]

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

        # Here s_last,a_last act as S,A
        self.delta = R - self.Q[(self.s_last,self.a_last)] # R - w_i (R is always 0 for WTTD)
        self.acc_z(self.z, self.s_last, self.a_last) # accumulating traces

        # Here s,a act as S',A'
        self.delta += 0 # terminal state fixed to value 0 for all actions
        for k in self.z.keys(): # all activated states
            # TODO: multiple by gamma where appropriate
            self.Q[k] += self.alpha*self.delta*self.z[k]
            self.z[k] = self.lmbda*self.z[k]

        self.s_last, self.a_last = None, None
        self.z = dict()
        self.delta = 0

if __name__ == "__main__":
    a = Sarsa_Lambda()
    f = open("Q.pkl", 'wb')
    a.save(f)
    a.load(f)
