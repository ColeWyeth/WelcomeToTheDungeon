from game import Game
from heroes import Warrior
from player import Player
from randomAgent import RandomAgent
import os
from datetime import datetime

from sarsa import Sarsa
from sarsa_lambda import Sarsa_Lambda

def training_arc(agent, episodes, playerNum = lambda e: 2):
    curr_session_name = "%s_%s" % (agent.name(), datetime.now())
    path = os.path.join(
            "training_sessions",
            curr_session_name,
    )
    os.makedirs(path)

    filename = "latest_model.pkl"
    filepath = os.path.join(path, filename)

    for episode in range(episodes):
        print("Beginning episode...")
        g = Game(Warrior(), [])
        agent_player = Player(agent)
        g.addPlayer(agent_player)
        for i in range(playerNum(episode)):
            if episode < 1000:
                g.addPlayer(Player(RandomAgent()))
            else:
                # Train against copies of the same agent 
                with open(filepath, 'rb') as f:
                    new_agent = agent.__class__(learning = False)
                    new_agent.load(f)
                    g.addPlayer(
                        Player(new_agent)
                    )
        #print(g.deck.cards)
        winner = g.run()
        agent_player.agent.terminateEpisode(winner == 0)

        if episode % 1000 == 0:
            with open(filepath, "wb") as f:
                agent_player.agent.save(f)

def test_against_random(agent, episodes, playerNum = lambda e: 2):
    print("Running %d test episodes against random opponents" % episodes)
    wins = 0
    for episode in range(episodes):
        g = Game(Warrior(), [])
        agent_player = Player(agent)
        g.addPlayer(agent_player)
        for i in range(playerNum(episode)):
            g.addPlayer(Player(RandomAgent()))
        #print(g.deck.cards)
        winner = g.run()
        agent_player.agent.terminateEpisode(winner == 0)
        if winner == 0:
            wins += 1
    print("%d wins out of %d" % (wins, episodes))

if __name__ == "__main__":
    a = Sarsa_Lambda()
    training_arc(a, 10000)
    test_against_random(a, 100)