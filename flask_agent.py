from agent import Agent
from waiting import wait

class FlaskAgent(Agent):
    def __init__(self):
        self.next_action = None

    def set_next_action(self, next_action):
        self.next_action = next_action

    def action(self, obs, actions, description=None):
        wait(
            lambda : not self.next_action is None,
            waiting_for="flask agent action",
        )
        action = self.next_action
        self.next_action = None
        return action        
