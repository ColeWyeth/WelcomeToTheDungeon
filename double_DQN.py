from agent import Agent
import torch
from bridge import vector_encoding
import pickle
import random
import numpy as np

class Q_net(torch.nn.Module):
    def __init__(self, in_dim, out_dim, hidden_units=20):
        torch.nn.Module.__init__(self)
        self.hidden1 = torch.nn.Linear(in_dim, hidden_units)
        self.hidden2 = torch.nn.Linear(hidden_units, hidden_units)
        self.ReLU = torch.nn.ReLU()
        self.output = torch.nn.Linear(hidden_units, out_dim)

    def forward(self, x):
        x = self.hidden1(x)
        x = self.ReLU(x)
        x = self.hidden2(x)
        x = self.ReLU(x)
        x = self.output(x)
        return x


# Algorithm from Hado van Hesselt, Arthur Guez, David Silver:
# Deep Reinforcement Learning with Double Q-learning
# (the implementation is mine)
class DoubleDQN(Agent):
    def __init__(self, learning = True, alpha=0.1, eps=0.1, buffSize = 1000):
        self.learning = learning
        self.alpha = alpha
        self.eps = eps
        self.buffSize = buffSize
        self.buffInd = 0
        # Vector encoding has 5 + 6 = 11 features
        # We also enter 1 action for 12 inputs
        self.Q = Q_net(12, 1)
        self.Q_target = Q_net(12, 1)
        self.playback_buffer = []
        self.sync_Q_target()
        self.bridge = lambda x: vector_encoding(self, x)
        # Previous state, action
        self.s_t = None
        self.a_t = None
        self.epochs_since_sync = 0
        self.since_refl = 0

    def action(self, obs, actions, description=None):
        s, r = self.bridge(obs)

        bestQVal = -float("inf")
        next_a = None
        for a in actions:
            a = int(a)
            x = torch.tensor(s + [a]).unsqueeze(dim=0).float()
            #print(x)
            QVal = self.Q(x).item()
            #print(QVal)
            if QVal > bestQVal:
                bestQVal = QVal
                next_a = a

        if self.learning:
            # Memorize this occurrence
            if not self.s_t is None:
                # Because the action set is not known in advance, 
                # I've been forced to modify this to work more like SARSA!
                # The chosen action is included in the replay buffer.
                # However, we still retain the spirit of Q learning,
                # because this is off-policy (epsilon greedy exploration
                # does not effect the a recorded).
                self.pushBuffer((self.s_t, self.a_t, r, s, a))

            # Time to do a little learning from experience
            if self.since_refl > 1000:
                self.reflect(100)
                self.since_refl = 0

        
        if random.random() < self.eps:
            next_a = random.choice(actions)   

        self.s_t = s
        self.a_t = next_a
        self.since_refl += 1
        return next_a
        
    def pushBuffer(self, entry):
        """The buffer overflows circularly (old memories are overwritten)."""
        if len(self.playback_buffer) < self.buffSize:
            self.playback_buffer.append(entry)
        else:
            self.playback_buffer[self.buffInd] = entry
            self.buffInd = (self.buffInd + 1) % len(self.playback_buffer)

    def sync_Q_target(self):
        self.Q_target.load_state_dict(self.Q.state_dict())

    def save(self, f):
        pickle.dump(self.Q.state_dict(), f)

    def load(self, f):
        self.Q.load_state_dict(pickle.load(f))
        self.sync_Q_target()

    def terminateEpisode(self, win=False):
        if self.learning:
            r = int(win)
            # The terminal state is a special case.
            # It will only be considered during learning, but have value 0
            s = -1
            if not self.s_t is None:
                self.pushBuffer((self.s_t, self.a_t, r, s, None))
            if self.since_refl > 1000:
                self.reflect(100)
                self.since_refl = 0
        self.s_t = None
        self.a_t = None

    def reflect(self, entries=100, epochs=5, batch_size=5):
        """This is where all learning from experience takes place."""
        if len(self.playback_buffer) < entries:
            return
        x_set = []
        y_set = []
        for e in range(entries):
            s_t, a_t, r, s_t1, a_t1 = random.choice(self.playback_buffer)
            if s_t1 == -1:
                state_eval = 0 # terminal state
            else:
                # a_t1 was chosen by an argmax over Q
                x = torch.tensor(s_t1 + [a_t1]).unsqueeze(dim=0).float()
                state_eval = self.Q_target(x)
            target = r + state_eval
            x_set.append(s_t + [a_t])
            y_set.append(target)
        x_set = torch.tensor(x_set).float()
        y_set = torch.tensor(y_set).float()
        train_set = [(x,y) for x, y in zip(x_set, y_set)]
        # there is a warning about size [5] v.s. [5, 1], not understood
        trainloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size)
        
        loss = torch.nn.MSELoss()
        optim = torch.optim.SGD(self.Q.parameters(), lr=0.00001)

        for epoch in range(epochs):
            for x, y in trainloader:
                #print("y:")
                #print(y)
                pred = self.Q(x)
                #print("pred:")
                #print(pred)
                l = loss(pred, y)
                #print("Loss:")
                #print(l)
                l.backward()
                optim.step()
            self.epochs_since_sync += 1

        if self.epochs_since_sync > 5:
            #print("Syncing")
            self.sync_Q_target()
            self.epochs_since_sync = 0
        
        