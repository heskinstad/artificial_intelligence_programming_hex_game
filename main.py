from Strategies import Strategies

strategy = "generate_data"
# Strategies
    # random - both players select random moves until end
    # mcts - both players select moves based on mcts with mcts parameters
    # generate_data - run n number of games and save data from every episode to the file data_filename
    # train_network - train data on n number of episodes based on the data_filename, save weights to weights_filename
    # train_networks - train a number of networks (size of save_interval up to num_episodes)
    # topp_tournament_2_players - TOPP tournament between two players

# Game parameters
board_size = 4
show_board = False
rollouts_per_episode = 600
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.0001  # Pause will be longer if time to run each episode > min_pause_length
c = 1.42  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
number_of_actual_games = 200  # How many games are to be played

data_filename = "gamedata/gamedata_" + str(board_size) + "x" + str(board_size) + "_board_" + str(number_of_actual_games) + "_games_" + str(rollouts_per_episode) + "_rollouts_" + str(c) + "c"

game_parameters = [board_size, show_board, rollouts_per_episode, node_expansion, min_pause_length, c, number_of_actual_games, data_filename]

# ANET parameters
save_interval = 2  # Save for each n number of actual games/episodes
num_epochs = 250  # Number of epochs in training
batch_size = 50  # Training batch size
optimizer = "adam"
loss = "categorical_crossentropy"
num_episodes = 1500  # Maximum number of episodes for the network to train on
learning_rate = 0.0025

weights_filename = "weights/weights_" + str(num_episodes) + "_episodes_" + str(num_epochs) + "_epochs.h5"

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, learning_rate]

# TOPP parameters
player1_id = 1
player2_id = 2
player1_weights_loc = "weights/weights_0_episodes_250_epochs.h5"
player2_weights_loc = "weights/weights_1500_episodes_250_epochs.h5"
number_of_topp_games = 100  # Should be dividable by 2 so that each player start first equal number of times

topp_parameters = [player1_id, player2_id, player1_weights_loc, player2_weights_loc, number_of_topp_games]



Strategies(strategy, game_parameters, anet_parameters, topp_parameters)

