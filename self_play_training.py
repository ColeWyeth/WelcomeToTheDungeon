from game import Game
from heroes import Warrior
from player import Player
from randomAgent import RandomAgent
import os
from datetime import datetime

from sarsa import Sarsa, Sarsa_NGram
from sarsa_lambda import Sarsa_Lambda, Sarsa_Lambda_NGram
from double_DQN import DoubleDQN, Double_DQN_NGram
from tqdm import tqdm

from bridge import vector_encoding
from short_term_memory import AddShortTermMemoryUnit

def training_arc(
    agent, 
    episodes,
    playerNum = lambda e: 2,
    eps_per_round=1000,
    self_play = True,
    ):
    curr_session_name = "%s_%s" % (agent.name(), datetime.now())
    path = os.path.join(
            "training_sessions",
            curr_session_name,
    )
    os.makedirs(path)

    filename = "latest_model.pkl"
    filepath = os.path.join(path, filename)

    eps_per_round = eps_per_round
    rounds = episodes//eps_per_round
    for round in range(rounds):
        print("Beginning round %d of training" % round)
        if round == 0 or not self_play:
            print("%s against random agents" % type(agent).__name__)
        else:
            print("%s against copies of itself" % type(agent).__name__)
        wins = 0
        for episode in tqdm(range(eps_per_round)):
            g = Game(Warrior(), [], verbose=False)
            agent_player = Player(agent)
            g.addPlayer(agent_player)
            for i in range(playerNum(episode)):
                if round == 0 or not self_play:
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
            if winner == 0:
                wins +=1

        print("%d wins out of %d games" % (wins, eps_per_round))

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
            print("Won a game")
        else:
            print("Lost a game")
    print("%d wins out of %d" % (wins, episodes))

if __name__ == "__main__":
    a = Double_DQN_NGram(bridge=vector_encoding(), size=2)
    training_arc(a, 30000, self_play=False)
    test_against_random(a, 100)