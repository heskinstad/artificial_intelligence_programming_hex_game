from Strategies import Strategies

strategy = "topp_mini"
# Strategies
    # random - both players select random moves until end
    # mcts - both players select moves based on mcts with mcts parameters
    # generate_data - run n number of games and save data from every episode to the file data_filename
    # train_network - train data on n number of episodes based on the data_filename, save weights to weights_filename
    # train_networks - train a number of networks (size of save_interval up to num_episodes)
    # topp_tournament_2_players - TOPP tournament between two players
    # topp_tournament
    # topp_mini

# Game parameters
board_size = 4
show_board = False
rollouts_per_episode = 40
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.00001  # Pause will be longer if time to run each episode > min_pause_length - 0.0006 for 7x7, 0.001 for 4x4
c = 1.42  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
number_of_actual_games = 200  # How many games are to be played

data_filename = "gamedata/gamedata_" + str(board_size) + "x" + str(board_size) + "_board_" + str(number_of_actual_games) + "_games_" + str(rollouts_per_episode) + "_rollouts_" + str(c) + "c"

game_parameters = [board_size, show_board, rollouts_per_episode, node_expansion, min_pause_length, c, number_of_actual_games, data_filename]

# ANET parameters
save_interval = 10  # Save for each n number of actual games/episodes
num_epochs = 250  # Number of epochs in training
batch_size = 50  # Training batch size
optimizer = "SGD"
loss = "categorical_crossentropy"
num_episodes = 1500  # Maximum number of episodes for the network to train on
learning_rate = 0.02  # Should be 0.001 for 4x4 with adam

weights_filename = "weights/weights_" + str(num_episodes) + "_episodes_" + str(num_epochs) + "_epochs.h5"

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, learning_rate]

# TOPP parameters
player1_id = 1
player2_id = 2
player1_weights_loc = "weights/TOPP_0.h5"
player2_weights_loc = "weights/TOPP_70.h5"
number_of_topp_games = 100  # Should be dividable by 2 so that each player start first equal number of times
save_folder = "topp_mini4"
topp_mini_games = 40

topp_parameters = [player1_id, player2_id, player1_weights_loc, player2_weights_loc, number_of_topp_games, save_folder, topp_mini_games]



Strategies(strategy, game_parameters, anet_parameters, topp_parameters)

