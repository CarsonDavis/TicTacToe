# TicTacToe
Standard TicTacToe game. Made to experiment with reinforcement deep learning.



### How to Play
Download the repository and run play_TicTacToe.py. 
Input your move as a number from 0-8, corresponding to the position on the board.

# Current Methodology
An initial model was trained on the data gathered from 25,000 random games. Only moves played by the winner of each game were used as training data.

A second model was trained by having the computer play itself in various configurations of random or using the initial model. Only moves played by the winner of each game were used as training data.

Details are recorded below:

Smart vs Random: 40k - kept all wins from both players - Wins: 38916 | 429 | 655

Random vs Smart: 40k - kept all wins from both players- Wins: 5962 | 33875 | 163

Random vs Random: 20k - kept all wins from both players - Wins: 11585 | 5900 | 2515

# Model Results on 10,000 Games

<b> BASELINE: Both players use random moves: </b>

First Player : 5842

Second Player : 2839

Ties: 1319


<b>First Player uses Model:</b>

First Player : 9745

Second Player : 103

Ties: 152


<b>Second Player uses Model:</b>

First Player : 1520

Second Player : 8451

Ties: 29


<b>Both Players use Model:</b>

First Player : 10000

Second Player : 0

Ties: 0

<b>Old Model vs New Model</b>

Smart v Old: 10000 | 0 | 0

Old v Smart: 10000 | 0 | 0

# Problems and Next Steps

These results seem functionally identical to the model trained only on random vs random games. 

Although this model does much better than randomly generated moves, especially when playing as Player 1, it is still not playing perfectly. 

A perfect model would never lose, and would always either win or tie. When played against itself, it would always tie. It would also win quickly, not choosing to block the oppenent instead of winning directly as the current model sometimes does.

As a next step, I am currently gathering data from the games where the model still manages to lose to a random player. I will figure out some way to empahsize those training examples and see if I can close the gaps in the model's strategy. 

If the results from that iteration are not satisfactory, then an additional step will be to give preferential treatment to fast games, where the model wins quickly.