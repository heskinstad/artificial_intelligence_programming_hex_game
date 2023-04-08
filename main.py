from Strategies import Strategies

board_size = 7
show_board = False
rollouts_per_episode = 500
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.01  # Pause will be longer if time to run each episode > min_pause_length
strategy = "anet"
c = 1.00  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
number_of_actual_games = 10  # How many games are to be played


# ANET parameters
optimizer = "adam"

anet_parameters = []

# OHT parameters


oht_parameters = []



Strategies(board_size, show_board, strategy, c, rollouts_per_episode, min_pause_length, node_expansion, number_of_actual_games)

