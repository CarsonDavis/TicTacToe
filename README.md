# TicTacToe
Standard TicTacToe game. Made to experiment with reinforcement deep learning.


### How to Play
Download the repository and run play_TicTacToe.py. 
Input your move as a number from 0-8, corresponding to the position on the board.

There is no error checking since human players are only for game verification. 


### First Training Methodology

For the first training, I had the computer play itself 25,000 times. Both players chose 
completely random moves. I only recorded games won by player 1. All moves made by 
player 1 in a won game are assumed to be good moves. A single training example consists 
of one board state and the move that player 1 played for that board state. Therefor the 
resulting model accepts a board state and outputs a move.

Further work will involve iterative play throughs using the trained models instead of 
random moves. The resulting data will be used to generate better models.


### First Training Results

<b> Both players use random moves: </b>

First Player : 14669

Second Player : 7145

Ties: 3186


<b>First Player uses Training Data:</b>

First Player : 22677

Second Player : 1080

Ties: 1243


<b>Second Player uses Training Data:</b>

First Player : 5588

Second Player : 16120

Ties: 3292


<b>Both Players use Training Data:</b>

First Player : 25000

Second Player : 0

Ties: 0