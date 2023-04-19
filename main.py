from Strategies import Strategies

# Game parameters
board_size = 4  # Size of board = board_size x board_size
visualize = [False, False]  # First is printing to the console, second is to its own cool window
rollouts_per_simulation = 40  # Rollouts per simulation in the MCTS during training
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.00001  # Pause will be longer if time to run each episode > min_pause_length - 0.0006 for 7x7, 0.001 for 4x4
c = 1.42  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)

game_parameters = [board_size, visualize, rollouts_per_simulation, node_expansion, min_pause_length, c]

# ANET parameters
save_interval = 10  # Save for each n number of actual games/episodes
num_epochs = 250  # Number of epochs in training
batch_size = 1024  # Training batch size
optimizer = "adam"
loss = "categorical_crossentropy"
num_episodes = 250  # Should be dividable by 2 so that each player start first equal number of times
learning_rate = 0.001  # Should be 0.001 for 4x4

anet_parameters = [save_interval, num_epochs, batch_size, optimizer, loss, num_episodes, learning_rate]

# TOPP parameters
player1_id = 1
player2_id = 2
M = 6  # Number of ANET models to save and play agains each other
topp_games_per_M = 50  # Number of games between every ANET model
anet_models_folder = "anet_models"
weights_episodes_multiplier = 10  # In TOPP tournament, player every weight trained on

topp_parameters = [player1_id, player2_id, M, topp_games_per_M, anet_models_folder, weights_episodes_multiplier]


Strategies(game_parameters, anet_parameters, topp_parameters)

