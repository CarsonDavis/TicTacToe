import numpy as np
import json
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras import models, layers, optimizers, losses, metrics
from make_data import make_data

# generate baseline data for the first training of the model
winning_boards, winner_history = make_data(model = None, iterations = 1000, probability=0)


print()
print('##############################################################################################################################################')
print('Winners of the intial random games')
print(f'Player 1: {winner_history[1]["wins"]/10} %')
print(f'Player 2: {winner_history[-1]["wins"]/10} %')
print(f'Tie Game: {winner_history["tie"]["wins"]/10} %')
print('##############################################################################################################################################')
print()

all_winning_boards = winning_boards['boards']
all_winning_moves = winning_boards['moves']

for model_iteration in range(50):

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

    print()
    print('##############################################################################################################################################')
    print('Evaluation new model on the validation data')
    print(model.evaluate(X_val, y_val))
    print()

    # run the new model to see how well it does when played 100% of the time
    ignore_me, winner_history = make_data(model = model, iterations = 1000, probability=1)
    
    # probability of player 1 using the model in the next training set is calculated by the percent games won or tied
    probability = (1000-winner_history[-1]['wins'])/1000
    # print(winner_history)
    # print('percent wins with new model', winner_history[1]['wins'])
    # print('probability to use new model in next data collection', probability)


    print('Win percentages with the new model')
    print(f'Player 1: {winner_history[1]["wins"]/10} %')
    print(f'Player 2: {winner_history[-1]["wins"]/10} %')
    print(f'Tie Game: {winner_history["tie"]["wins"]/10} %')
    print()
    print(f'Probabilty of using new model in the next data collection {probability}')
    print('##############################################################################################################################################')
    print()

    # use the new model to collect new data. also use random moves to as a proxy for creativity
    winning_boards, winner_history = make_data(model = model, iterations = 1000, probability=probability)

    # add newly generated training data to the corpus
    all_winning_boards += winning_boards['boards'].copy()
    all_winning_moves += winning_boards['moves'].copy()



