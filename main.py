from Strategies import Strategies

board_size = 7
show_board = False
rollouts_per_episode = 100
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.01  # Pause will be longer if time to run each episode > min_pause_length
strategy = "train_network"
c = 1.00  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
number_of_actual_games = 3  # How many games are to be played

data_filename = "gamedata_" + str(number_of_actual_games) + "_games_" + str(rollouts_per_episode) + "_rollouts"

# ANET parameters
save_interval = 2  # Save for each n number of actual games/episodes
num_epochs = 250
batch_size = 32
optimizer = "adadelta"
loss = "categorical_crossentropy"
num_episodes = 250

weights_filename = "weights_" + str(num_episodes) + "_episodes_" + str(num_epochs) + "_epochs.h5"

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, board_size*board_size+1, weights_filename]

# OHT parameters


oht_parameters = []



Strategies(board_size, show_board, strategy, c, rollouts_per_episode, min_pause_length, node_expansion, number_of_actual_games, data_filename, anet_parameters)

