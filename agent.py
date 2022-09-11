class Agent:
    def __init__(self):
        pass

    def setPInd(self, ind):
        self.pInd = ind 

    def name(self):
        return self.__class__.__name__

    def action(self, obs, actions, description=None):
        pass

    def terminateEpisode(self, win=False):
        pass

    def save(self, f):
        pass
    
    def load(self, f):
        pass

    def applyBridge(self, obs):
        return self.bridge(self, obs)

    def setBridge(self, bridge):
        self.bridge = bridge