import numpy as np
import json
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras import models, layers, optimizers, losses, metrics
from make_data import make_data


def train_model(boards, moves, model_name):

    # format and split the data
    X = np.array(boards)
    y = to_categorical(moves)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.2, random_state=42)

    # define the neural network
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
    # print('\n##############################################################################################################################################')
    print(f'Training of {model_name} {model_iteration + 1}\n')

    model.fit(X_train,
              y_train,
              epochs=10,
              batch_size = 1024,
              validation_data = (X_test, y_test))

    # print evaluation statistics
    print(f'\nEvaluation of {model_name} {model_iteration + 1}')
    print(model.evaluate(X_val, y_val), '\n')

    return model


# generate baseline data for the first training of the model
winning_data, losing_data, winner_history = make_data(winning_model = None, 
                                                      losing_model =  None, 
                                                      iterations = 1000, 
                                                      probability = 0)
all_winning_boards = winning_data['boards']
all_winning_moves = winning_data['moves']
all_losing_boards = losing_data['boards']
all_losing_moves = losing_data['moves']


# print random win statistics
print('\n##############################################################################################################################################')
print('Winners of the intial random games')
print(f'Player 1: {winner_history[1]["wins"]/10} %')
print(f'Player 2: {winner_history[-1]["wins"]/10} %')
print(f'Tie Game: {winner_history["tie"]["wins"]/10} %')
print('##############################################################################################################################################\n')


# iterate the model training
for model_iteration in range(5):

    winning_model = train_model(boards = all_winning_boards, 
                                moves = all_winning_moves,
                                model_name = 'Winning Model')

    losing_model = train_model(boards = all_losing_boards, 
                               moves = all_losing_moves,
                               model_name = 'Losing Model')

    # run the new models to see how well they do when played 100% of the time
    ignore_data, ignore_data, winner_history = make_data(winning_model = winning_model, 
                                                         losing_model =  losing_model, 
                                                         iterations = 1000, 
                                                         probability = 1)

    # probability of player 1 using the model in the next training set is calculated by the percent games won or tied
    probability = ((1000-winner_history[-1]['wins'])/1000)

    print(f'Win percentages against a random opponent using model {model_iteration + 1}')
    print(f'Player 1: {winner_history[1]["wins"]/10} %')
    print(f'Player 2: {winner_history[-1]["wins"]/10} %')
    print(f'Tie Game: {winner_history["tie"]["wins"]/10} %\n')
    print(f'Probabilty of using new model in the next data collection {probability}')
    print('##############################################################################################################################################\n')

    # use the new model to collect new data. also use random moves to as a proxy for creativity
    winning_data, losing_data, winner_history = make_data(winning_model = winning_model, 
                                                          losing_model =  losing_model, 
                                                          iterations = 1000, 
                                                          probability = probability)

    # add newly generated training data to the corpus
    all_winning_boards += winning_data['boards'].copy()
    all_winning_moves += winning_data['moves'].copy()
    all_losing_boards += losing_data['boards'].copy()
    all_losing_moves += losing_data['moves'].copy()

# winning_model.save('blahblah.h5')



