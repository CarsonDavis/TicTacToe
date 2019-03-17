# TicTacToe
Standard TicTacToe game. Made to experiment with reinforcement deep learning.



### How to Play
Download the repository and run play_TicTacToe.py. 
Input your move as a number from 0-8, corresponding to the position on the board.

# Current Model that Never Loses

After some experimentation and a huge 500,000 game training set, I was able to make a model (all_possible_games_3.h5) that never loses.
I made several other similar models which lose only 1 game path out of all possible TicTacToe games.
I don't consider this method to be extensible to other games, since 500k is not only a huge training set for other games, but it is also double the total number of unique tictactoe games. I don't think this is much different from brute forcing the solution. However, this was a useful exercise, since it demonstrates that the deep learning approach can work given enough data. 

It is important to note that even though the model never loses, it doesn't win quite as many games as some of the other models that I made, which means that there are probably 1 or 2 game paths where it could have won, but played the wrong move and tied instead.

# Next Steps

I will make a recursive trainer that plays small batches of games and then retrains the model, updating its strategy with every iteration. To prevent stagnation, I will have the model player alternate between using random moves and the current model. As model performance increases, the percent of random moves will be decreased until the model no longer loses games against a random player.

I hope to play around with this method and try to minimize the total number of training games required before the model never loses. I also want to create a model that never misses a win, and which ties against itself.

# Old Information Below

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

After finishing the initial experiments, I will make a recursive trainer that plays small batches of games and then retrains the model, updating its strategy with every iteration. To prevent stagnation, I will have the model player alternate between using random moves and the current model. As model performance increases, the percent of random moves will be decreased until the model no longer loses games against a random player.
