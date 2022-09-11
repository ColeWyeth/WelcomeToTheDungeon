from copy import deepcopy
from equipment import WARRIOR_ITEM_NAMES

class minimal_bridge:
    def __init__(self):
        self.dimension = 6

    def __call__(self, agent, obs):
        s = deepcopy(obs)

        if s["monsterDrawn"] is None:
            md = None
        else:
            md = s["monsterDrawn"]["strength"]
        
        # Agents are informed of their index when the game starts
        pInf = s["players"][agent.pInd]

        s = (
            s["dungeonSize"],
            md,
            s["currItemCode"],
            len(s["hero"]["items"]),
            pInf["successes"],
            pInf["failures"],
        )
        return s, 0 # the reward is always 0 for nonterminal states

class medium_bridge:
    def __init__(self):
        self.dimension = 6

    def __call__(self, agent, obs):
        s = deepcopy(obs)

        if s["monsterDrawn"] is None:
            md = None
        else:
            md = s["monsterDrawn"]["strength"]
        
        # Agents are informed of their index when the game starts
        pInf = s["players"][agent.pInd]

        s = (
            s["dungeonSize"],
            md,
            s["currItemCode"],
            s["hero"]["items"],
            pInf["successes"],
            pInf["failures"],
        )
        return s, 0 # the reward is always 0 for nonterminal states


# TODO: This encoding assumes the Warrior's equipment
class vector_encoding:
    def __init__(self):
        self.dimension = 11

    def __call__(self, agent, obs):
        """Medium bridge but encoded as a vector of real numbers."""
        s = deepcopy(obs)
        
        if s["monsterDrawn"] is None:
            md = 0
        else:
            md = s["monsterDrawn"]["strength"]

        if s["currItemCode"] is None:
            currItem = -1
        else:
            currItem = s["currItemCode"]
        
        # Agents are informed of their index when the game starts
        pInf = s["players"][agent.pInd]

        equipmentList = [e["name"] for e in s["hero"]["items"]]
        equipmentVec = [
            int(name in equipmentList) for name in WARRIOR_ITEM_NAMES
        ]

        s = [
            s["dungeonSize"],
            md,
            currItem,
            pInf["successes"],
            pInf["failures"],
        ]
        s.extend(equipmentVec)

        return s, 0 # the reward is always 0 for nonterminal states

class memory_bridge:
    def __init__(self, bridge, stmu):
        self.base_bridge = bridge
        self.dimension = bridge.dimension * stmu.size
    
    def __call__(self, agent, obs):
        o, r = self.base_bridge(agent, obs)
        agent.stmu.add(o)
        return agent.stmu.getFlattened(), r