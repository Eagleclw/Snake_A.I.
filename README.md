# Snake A.I.

A snake game powered with **Q-Learning** algorithm of **Reinforcement Learning** Method.  
**Developed with Python**.  

# Q-Learning

Q-Learning algorithm is an algorithm based on comparing experiences and choosing the best of them to act.  
The goal of the algorithm is find the best action to maximize the reward.  

It uses a state-reward table which called **Q-Table**.  
If current state doesn't exist in Q-Table, algorithm makes a **randomized** action and learn from it.  
If current state exist in Q-Table but after acting that action, reward is different, then it updates the Q-Table with newly learned state-rewards.  

# How It Works ?

**Rewards for this game**
* If Snake eats the food = +1.0 point reward
* If Snake eats itself = -1.0 point reward
* If Snake does nothing = -0.1 point reward  

**Updating Q-Table**
* Q = Q-Learning Table  
* act = The action user choosed  
* s0 = Current State  
* s1 = Next State (After making the action)  
* lr = Learning rate of A.I.  
* r = Reward of action  
* df = Discount factor

> Q[s0][act] = Q(s0)[act] + lr * (r + df * max(Q(s1)) - Q(s0)[act])  

## Game Basics

When user starts the game, a menu shows up.  
User can choose either **'Play as a Player'** or **'Train the A.I.'**.  

At **'Play as a Player'** side, user plays the game and makes the actions.  
While user plays the game, A.I. observes the actions that player made, updates the Q-Table and learns from it.  

At **'Train the A.I.'** side, A.I. plays the game by itself without any help.  
It chooses the best action available or makes a randomized action, updates the Q-Table and learns from it.  

To make A.I. learn faster, i created a 10x10 game area.  
If game area gets bigger (20x20 etc.), it gets longer to train the A.I. but results would be better aswell.  

When the game starts, it checks if there is saved game data.  
If there is, it loads the data. If there is no data, it creates them from initials.  
When user closes the game, it saves the data to a **JSON** file.  
So, best scores at game, A.I. states won't be lost.

## Usage

* **Arrow keys** to move (Up,Right,Down,Left)
* **Left Click** to choose menu options
* **P** key to **Pause** the game
* **S** key to **Speed Up the A.I.** for training faster  
Normal Play Speed : 10  
Speeded Up Play Speed : 1.000.000.000
* **Q** key to **Quit** the game (Return to Menu)  

## Installation
Clone or download the files.  
Open the files at an IDE (PyCharm etc.) or run from command line.  
**main.py** is the main game file to run.  

**NOTE: If you don't want to lose saved game data, first you should change directory to game's directory.**
* Windows = cd "path\to\snake\game"
* Linux / MacOS = cd path/to/snake/game  

**Commands to run the game from command line**
* Windows = "path\to\python\python.exe" "path\to\snake\game\main.py"  
For example = ("C:\Program Files (x86)\Python38-32\python.exe" "C:\Users\Eagleclw\Desktop\Snake\main.py")
* Linux / MacOS = python3 path/to/snake/game/main.py  

## License
[MIT](https://github.com/Eagleclw/Snake_A.I./blob/master/LICENSE)
