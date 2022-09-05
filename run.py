from flask import Flask 
from flask import request
from flask_cors import CORS
from game import Game 
from player import Player
from flask_agent import FlaskAgent
from randomAgent import RandomAgent
from terminalAgent import TerminalAgent
from sarsa import Sarsa
from sarsa_lambda import Sarsa_Lambda
from double_DQN import DoubleDQN
from heroes import Warrior
from threading import Thread 
import os
import json

app = Flask(__name__)
CORS(app)

game_records = dict()

@app.route('/join_game', methods=['GET', 'POST'])
def join_game():
    gameID = request.form.get("GameID");
    if gameID in game_records.keys():
        print("Game already exists")
    else:
        print("Creating game")
        g = Game(Warrior(), [])
        game_records[gameID] = {"game":g, "online_players":{}, "started":False, "thread": None}
    g = game_records[gameID]["game"]
    online_player = Player(FlaskAgent())
    g.addPlayer(online_player)
    game_records[gameID]["online_players"][request.form.get("PlayerName")] = online_player
    print("Game ID %s, added player %s" % (gameID, request.form.get("PlayerName")))
    return("Success")

@app.route('/add_ai_player', methods=['GET','POST'])
def addAIPlayer():
    print("Received request to add a new AI Player")
    gameID = request.form.get("GameID")
    playerType = request.form.get("PlayerType")
    if not gameID in game_records.keys():
        err_msg = "Failure: There is no game with this ID: "
        print(err_msg)
        return(err_msg)
    g = game_records[gameID]["game"]
    if playerType == "Random":
        msg = "Adding random player"
        print(msg)
        g.addPlayer(Player(RandomAgent()))
        return(msg)
    elif playerType == "Sarsa":
        msg = "Adding Sarsa player"
        print(msg)
        sa = Sarsa()
        sa.load(
            open(
                os.path.join("example_agents", "Sarsa_rec.pkl"),
                'rb'
            ),
        )
        sp = Player(sa)
        g.addPlayer(sp)
        return(msg)
    elif playerType == "SarsaLambda":
        msg = "Adding Sarsa Lambda Player"
        print(msg)
        sla = Sarsa_Lambda()
        sla.load(
            open(
                os.path.join("example_agents", "Sarsa_Lambda_rec.pkl"),
                'rb'
            ),
        )
        slp = Player(sla)
        g.addPlayer(slp)
        return(msg)
    elif playerType == "DoubleDQN":
        msg = "Addding Double DQN player"
        print(msg)
        dqna = DoubleDQN(learning=False)
        dqna.load(
            open(
                os.path.join("example_agents", "Double_DQN.pkl"),
                'rb'
            ),
        )
        dqnp = Player(dqna)
        g.addPlayer(dqnp)
        return(msg)
    else:
        return("Player type not recognized")

@app.route('/start_game', methods=['GET','POST'])
def start_game():
    gameID = request.form.get("GameID")
    if not gameID in game_records.keys():
        err_msg = "Failure: There is no game with this ID"
        print(err_msg)
        return(err_msg)
    elif game_records[gameID]["started"]:
        msg = "Game already started"
        print(msg)
        return(msg)
    g = game_records[gameID]["game"]
    def runGame():
        g.run()
    t = Thread(target=runGame)
    t.start()
    game_records[gameID]["started"] = True 
    game_records[gameID]["thread"] = t
    return("Game started:\n" + str(g))

@app.route('/game_state', methods=['GET', 'POST'])
def state():
    g = game_records[request.form.get("GameID")]["game"]
    return g.getJson()

@app.route('/action', methods=['GET','POST'])
def action():
    gameID = request.form.get("GameID")
    playerName = request.form.get("PlayerName")
    online_player = game_records[gameID]["online_players"][playerName]
    online_player.agent.set_next_action(int(request.form.get("action")))
    return("Action set to " + request.form.get("action"))

@app.route('/history', methods=['GET','POST'])
def history():
    gameID = request.form.get("GameID")
    g = game_records[gameID]["game"]
    h = g.history
    g.history = []
    return(str({"history" : h}))

@app.route('/log', methods=['GET','POST'])
def getLog():
    gameID = request.form.get("GameID")
    g = game_records[gameID]["game"]
    return(g.log)
    
@app.route('/player_names', methods=['GET', 'POST'])
def names():
    """Returns the names of each player in index order, as json converted list."""
    gameID = request.form.get("GameID")
    if not gameID in game_records.keys():
        err_msg = "Failure: There is no game with this ID: "
        print(err_msg)
        return(err_msg)
    online_players = game_records[gameID]["online_players"]
    g = game_records[gameID]["game"]
    players = g.players
    # correlate player names with player IDs
    name_id_list = []
    for p in players:
        online = False
        for k in online_players.keys():
            if online_players[k] == p:
                online = True
                name_id_list.append((k, p.agent.pInd))
        if not online:
            name_id_list.append((p.agent.name(), p.agent.pInd))
    name_id_list.sort(key = lambda x: x[1])
    return json.dumps([x[0] for x in name_id_list])

def runFlask():
    app.run()


if __name__=="__main__":
    runFlask()