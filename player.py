from enum import Enum

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

    def action(self, obs, actions=None, description=None):
        """
        obs must include everything an agent might need to know to understand
        the meaning of each action in the current situation.
        description is English text included for terminal players.
        """
        return self.agent.action(obs, actions, description=description)

    def isActive(self):
        return self.state.active

    def takeLoss(self):
        self.state.failures += 1
    
    def takeWin(self):
        self.state.successes += 1