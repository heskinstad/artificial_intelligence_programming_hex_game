from Strategies import Strategies

board_size = 7
show_board = True
min_pause_length = 2.0  # Pause will be longer if time to run each episode > min_pause_length
strategy = "mcts"
#TODO: add variable to determine how much the tree should expand for each "floor"
c = 1.0  # The higher this value is, the more likely the players are to try less optimal nodes (more exploration)
M = 2.0  # Max time per actual move in seconds

Strategies(board_size, show_board, strategy, c, M, min_pause_length)

