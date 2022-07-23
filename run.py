from flask import Flask 
from flask import request
from game import Game 
from player import Player
from flask_agent import FlaskAgent
from randomAgent import RandomAgent
from terminalAgent import TerminalAgent
from heroes import Warrior
from threading import Thread 

app = Flask(__name__)

game_records = []

@app.route('/start_game', methods=['GET', 'POST'])
def start_game():
    g = Game(Warrior(), [])
    online_player = Player(FlaskAgent())
    g.addPlayer(online_player)
    game_records.append({"game":g, "online_players":[online_player]})

    def runGame():
        print("Entered main loop")
        while True:
            winner = g.checkForWinner()
            if not winner is None:
                print("Player %d won!" % winner)
                break
            g.step()

    if request.method == 'POST' or request.method == 'GET':
        # for p in ["p1", "p2"]:
        #     if request.form.get(p) == "RandomAgent":
        #         g.addPlayer(Player(RandomAgent()))
        g.addPlayer(Player(RandomAgent()))
        t = Thread(target=runGame)
        t.start()
        return("Game started:\n" + str(g))
    return("Game not started")

@app.route('/game_state', methods=['GET', 'POST'])
def state():
    g = game_records[0]["game"]
    return g.getJson()

@app.route('/action', methods=['GET','POST'])
def action():
    online_player = game_records[0]["online_players"][0]
    online_player.agent.set_next_action(int(request.form.get("action")))
    return("Action set to " + request.form.get("action"))

@app.route('/history', methods=['GET','POST'])
def history():
    g = game_records[0]["game"]
    h = g.history
    g.history = []
    return(str({"history" : h}))

def runFlask():
    app.run()


if __name__=="__main__":
    runFlask()