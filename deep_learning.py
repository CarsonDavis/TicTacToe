import numpy as np
import json
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras import models, layers, optimizers, losses, metrics
from make_data import make_data

winning_boards, winner_history = make_data(model = None, iterations = 1000, probability=0)

print()
print('##############################################################################################################################################')
print('results of the initial random games')
print(winner_history)
print('wins using random', winner_history[1]['wins'])
print('##############################################################################################################################################')
print()


for model_iteration in range(5):

    X = np.array(winning_boards['boards'])
    y = to_categorical(winning_boards['moves'])

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

    probability = (winner_history[1]['wins']/1000)
    print('probability to use with new model', probability)
    winning_boards, winner_history = make_data(model = model, iterations = 1000, probability=probability)
    print('wins with new model', winner_history[1]['wins'])
    print('##############################################################################################################################################')
    print()

# for player in winner_history.keys():
#     print(winner_history[player]['name'], winner_history[player]['wins'])