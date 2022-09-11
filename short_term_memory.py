from bridge import memory_bridge

class ShortTermMemoryUnit:
    def __init__(self, dimension, size, empty=0, hashable=False):
        self.idx = 0
        self.size = size
        self.dimension = dimension
        self.empty = empty
        self.setBlank()
        self.hashable = hashable
        

    def setBlank(self):
        self.memories = [[self.empty for d in range(self.dimension)] for s in range(self.size)]

    def add(self, memory):
        self.memories.append(memory)
        if len(self.memories) > self.size:
            self.memories.pop(0)

    def getFlattened(self):
        flattened = []
        for memory in self.memories:
            flattened.extend(memory)
        if self.hashable:
            flattened = tuple(flattened)
        return flattened

def AddShortTermMemoryUnit(agent, size, empty=0, hashable=False):
    dim = agent.bridge.dimension
    stmu = ShortTermMemoryUnit(dim, size, empty, hashable)
    agent.stmu = stmu
    agent.setBridge(memory_bridge(agent.bridge, agent.stmu))
    return agent