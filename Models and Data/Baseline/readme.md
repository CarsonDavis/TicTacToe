# this model never loses, although it seems a bit worse in various ways to model 3462
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics

model = models.Sequential()

model.add(layers.Dense(729, activation = 'relu', input_shape = (9,)))
model.add(layers.Dense(729, activation = 'relu'))
model.add(layers.Dense(729, activation = 'relu'))
model.add(layers.Dense(729, activation = 'relu'))
model.add(layers.Dense(81, activation = 'relu'))
model.add(layers.Dense(81, activation = 'relu'))
model.add(layers.Dense(81, activation = 'relu'))
model.add(layers.Dense(81, activation = 'relu'))
model.add(layers.Dense(9, activation = 'softmax'))


model.compile(optimizer = 'rmsprop',
             loss = 'categorical_crossentropy',
             metrics = ['accuracy'])


# train the network
now = time.time()

history = model.fit(X_train,
                   y_train,
                   epochs=6,
                   batch_size = 5120,
                   validation_data = (X_test, y_test))

print(model.evaluate(X_val, y_val))
model.save('all_possible_games_3.h5')


9831 | 0 | 169
1122 | 8819 | 59 


















using model 3462
    "new_model.add(layers.Dense(729, activation = 'relu', input_shape = (9,)))\n",
    "new_model.add(layers.Dense(729, activation = 'relu'))\n",
    "new_model.add(layers.Dense(729, activation = 'relu'))\n",
    "new_model.add(layers.Dense(81, activation = 'relu'))\n",
    "new_model.add(layers.Dense(81, activation = 'relu'))\n",
    "new_model.add(layers.Dense(81, activation = 'relu'))\n",
    "new_model.add(layers.Dense(9, activation = 'softmax'))\n",

    i think ^

9881 | 53 | 66

1053 | 8922 | 25


There seems to be only one game where it loses
Player 1's Move
0 0 0
0 0 0
0 0 0

Player 2's Move
0 0 0
0 1 0
0 0 0

2
Player 1's Move
0 0 -1
0 1 0
0 0 0

Player 2's Move
0 0 -1
0 1 0
0 0 1

0
Player 1's Move
-1 0 -1
0 1 0
0 0 1

Player 2's Move
-1 0 -1
0 1 0
0 1 1

1
-1 -1 -1
0 1 0
0 1 1

Player 2  wins!