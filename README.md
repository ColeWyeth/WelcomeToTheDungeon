# WelcomeToTheDungeon
An implementation of the board game "Welcome to the Dungeon" with RL based A.I. players.  

To communicate with a game over flask:

Run run.py
Send any request to /start_game. Currently this starts a game against a random agent.
Send any request to /game_state to get the game state
Send any request to /history to see past states since the last time you got the history
Send an action to /action to take that action. Depending on the situation the options are:
    0/1 for don't pass, pass
    -1 or the index of an item for adding a monster or removing an equipment
    x to defeat monsters of strength x with the Vorpal sword
This should be the action field of the body of your request (in insomnia I use a Multipart request).

You can play against the sarsa and sarsa lambda agents on my website at https://colewyeth.com/welcome_to_the_dungeon.html.
The UI is slightly fragile so may require some reloads. Use a large random game ID and add at most two opponents to the game.
The Double DQN agent is also functional but is not served online due to memory requirements.
