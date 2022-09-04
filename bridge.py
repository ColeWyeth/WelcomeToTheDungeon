from copy import deepcopy
from equipment import WARRIOR_ITEM_NAMES

def minimal_bridge(self, obs):
    s = deepcopy(obs)

    if s["monsterDrawn"] is None:
        md = None
    else:
        md = s["monsterDrawn"]["strength"]
    
    # Agents are informed of their index when the game starts
    pInf = s["players"][self.pInd]

    s = (
        s["dungeonSize"],
        md,
        s["currItemCode"],
        len(s["hero"]["items"]),
        pInf["successes"],
        pInf["failures"],
    )
    return s, 0 # the reward is always 0 for nonterminal states

def medium_bridge(self, obs):
    s = deepcopy(obs)

    if s["monsterDrawn"] is None:
        md = None
    else:
        md = s["monsterDrawn"]["strength"]
    
    # Agents are informed of their index when the game starts
    pInf = s["players"][self.pInd]

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
def vector_encoding(self, obs):
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
    pInf = s["players"][self.pInd]

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