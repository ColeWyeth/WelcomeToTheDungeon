from flask import Flask 
from game import Game 
from player import Player
from randomAgent import RandomAgent
from terminalAgent import TerminalAgent
from heroes import Warrior
from threading import Thread 

players = [Player(RandomAgent()) for i in range(6)]
g = Game(Warrior(), players)
g.addPlayer(Player(TerminalAgent()))
print(g)

app = Flask(__name__)

@app.route('/')
def index():
    return g.getJson()

def runFlask():
    app.run()

def runGame():
    print("Entered main loop")
    while True:
        winner = g.checkForWinner()
        if not winner is None:
            print("Player %d won!" % winner)
            break
        g.step()

if __name__=="__main__":
    t = Thread(target=runGame)
    t.start()
    runFlask()