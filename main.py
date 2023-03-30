from Strategies import Strategies

board_size = 7
show_board = False
rollouts_per_episode = 1000
node_expansion = 1  # Determines how much the tree should expand for each "floor". Expands to max_number_of_nodes_left / node_expansion
min_pause_length = 0.001  # Pause will be longer if time to run each episode > min_pause_length
strategy = "mcts"
c = 1.00  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)

Strategies(board_size, show_board, strategy, c, rollouts_per_episode, min_pause_length, node_expansion)

