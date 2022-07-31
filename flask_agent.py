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
        a = self.next_action
        if a in actions:
            action = a
        else:
            print("Invalid choice, taking first action")
            action = actions[0]
        self.next_action = None
        return action        
