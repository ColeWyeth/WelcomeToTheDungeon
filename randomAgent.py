import random
from agent import Agent

class RandomAgent(Agent):
    def action(self, obs, actions, description=None):
        if actions is None:
            raise Exception("The random agent requires an action list")
        return(random.choice(actions))