from make_data import make_data
from keras.models import load_model

for i in range(10): 
        
    winning_model = load_model(f'Models and Data/Recursive Models/{i}_winning.h5')
    losing_model = load_model(f'Models and Data/Recursive Models/{i}_losing.h5')

    winning_data, losing_data, winner_history = make_data(winning_model, losing_model, iterations= 1000, probability=1)

    print('\n##############################################################################################################################################')
    print('Winners of the intial random games')

    print(i)
    print(f'Player 1: {winner_history[1]["wins"]/10} %')
    print(f'Player 2: {winner_history[-1]["wins"]/10} %')
    print(f'Tie Game: {winner_history["tie"]["wins"]/10} %')
    print('##############################################################################################################################################\n')
