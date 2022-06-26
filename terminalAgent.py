from agent import Agent

class TerminalAgent(Agent):
    def action(self, obs, actions, description="Enter action: "):
        print("Observed state: " + str(obs))
        a = int(input(description))
        if a in actions:
            return a
        else:
            print("Invalid choice, taking first action")
            return actions[0]