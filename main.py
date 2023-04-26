import multiprocessing

from Strategies import Strategies
import tensorflow as tf

# Game parameters
board_size = 7  # Size of board = board_size x board_size
visualize = [False, False]  # First is printing to the console, second is to its own cool window
rollouts_per_simulation = 10  # Rollouts per simulation in the MCTS during training
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.0  # Pause will be longer if time to run each episode > min_pause_length - 0.0006 for 7x7, 0.001 for 4x4
c = 1.42  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)

game_parameters = [board_size, visualize, rollouts_per_simulation, node_expansion, min_pause_length, c]

# ANET parameters
save_interval = 10  # Save for each n number of actual games/episodes
num_epochs = 1000  # Number of epochs in training - an article stated 11 is a good starting point.
batch_size = 100000  # Training batch size
optimizer = "adam"
loss = "categorical_crossentropy"
num_episodes = 1500  # Number of episodes to generate data for
learning_rate = 0.001  # Should be 0.001 for 4x4
num_of_hidden_layers = 3
num_of_neurons_per_layer = 100

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, learning_rate, num_of_hidden_layers, num_of_neurons_per_layer]

# TOPP parameters
player1_id = 1
player2_id = 2
M = 6  # Number of ANET models to play against each other
topp_games_per_M = 50  # Number of games between every ANET model. Should be dividable by 2 so that each player start first equal number of times
model_episodes_multiplier = 50  # In TOPP tournament, player every weight trained on
anet_models_folder = "oht_models"

topp_parameters = [player1_id, player2_id, M, topp_games_per_M, anet_models_folder, model_episodes_multiplier]


duel1 = 0
duel2 = 50
duel_extra_parameters = [duel1, duel2]

anets = [0, 50, 100, 150, 200, 250]  # Designate the anet models to compete in the TOPP_CUSTOM with the number of episodes they've been trained on

# Strategies: TOPP (TOPP tournament), TOPP_CUSTOM (TOPP between pre-trained anet models) or DUEL (have two models play against each other)
strategy = "GEN_DATA"

tete = Strategies(strategy, game_parameters, anet_parameters, topp_parameters, duel_extra_parameters, anets, "tete.h5", 20)

'''
def new_function(tete):
    Strategies(strategy, game_parameters, anet_parameters, topp_parameters, duel_extra_parameters, anets, "tete.h5", tete)

def thread_function(n):
    return new_function(multiprocessing.current_process().pid)

def main(n):
    with multiprocessing.Pool(processes=n) as pool:
        results = pool.map(thread_function, range(n))

if __name__ == '__main__':
    n = 20  # The number of processes to use
    main(n)

'''