import numpy as np
import json
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras import models, layers, optimizers, losses, metrics
from make_data import make_data

winning_boards, model_test = make_data(model = None, iterations = 1000, probability=0)
probability = .5


print()
print('##############################################################################################################################################')
print('results of the initial random games')
print(model_test)
print('wins using random', model_test[1]['wins'])
print('##############################################################################################################################################')
print()

all_winning_boards = winning_boards['boards']
all_winning_moves = winning_boards['moves']

for model_iteration in range(10):

    X = np.array(all_winning_boards)
    y = to_categorical(all_winning_moves)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.2, random_state=42)

    model = models.Sequential()

    model.add(layers.Dense(729, activation = 'relu', input_shape = (9,)))
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
    history = model.fit(X_train,
                    y_train,
                    epochs=10,
                    batch_size = 512,
                    validation_data = (X_test, y_test))

    print(model.evaluate(X_val, y_val))

    
    print('probability to use with new model', probability)
    winning_boards, winner_history = make_data(model = model, iterations = 1000, probability=probability)
    ignore_me, model_test = make_data(model = model, iterations = 1000, probability=1)
    print('wins with new model', model_test[1]['wins'])
    print('##############################################################################################################################################')
    print()

    probability = (model_test[1]['wins']/1000)
    all_winning_boards += winning_boards['boards'].copy()
    all_winning_moves += winning_boards['moves'].copy()
