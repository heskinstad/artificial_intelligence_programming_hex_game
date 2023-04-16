from Strategies import Strategies

strategy = "mcts"
# Strategies
    # random - both players select random moves until end
    # mcts - both players select moves based on mcts with mcts parameters
    # generate_data - run n number of games and save data from every episode to the file data_filename
    # train_network - train data on n number of episodes based on the data_filename, save weights to weights_filename
    # train_networks - train a number of networks (size of save_interval up to num_episodes)
    # topp_tournament_2_players - TOPP tournament between two players

# Game parameters
board_size = 7
show_board = False
rollouts_per_episode = 1500
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.01  # Pause will be longer if time to run each episode > min_pause_length
c = 0.0  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
number_of_actual_games = 50  # How many games are to be played

data_filename = "gamedata/gamedata_" + str(number_of_actual_games) + "_games_" + str(rollouts_per_episode) + "_rollouts_" + str(c) + "c"

game_parameters = [board_size, show_board, rollouts_per_episode, node_expansion, min_pause_length, c, number_of_actual_games, data_filename]

# ANET parameters
save_interval = 2  # Save for each n number of actual games/episodes
num_epochs = 250  # Number of epochs in training
batch_size = 32  # Training batch size
optimizer = "adadelta"
loss = "categorical_crossentropy"
num_episodes = 250  # Maximum number of episodes for the network to train on

weights_filename = "weights/weights_" + str(num_episodes) + "_episodes_" + str(num_epochs) + "_epochs.h5"

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename]

# TOPP parameters
player1_id = 1
player2_id = 2
player1_weights_loc = "weights/weights_0_episodes_250_epochs.h5"
player2_weights_loc = "weights/weights_250_episodes_250_epochs.h5"
number_of_topp_games = 100  # Should be dividable by 2 so that each player start first equal number of times

topp_parameters = [player1_id, player2_id, player1_weights_loc, player2_weights_loc, number_of_topp_games]



Strategies(strategy, game_parameters, anet_parameters, topp_parameters)

