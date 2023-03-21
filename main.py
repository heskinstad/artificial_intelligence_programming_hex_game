from Strategies import Strategies

board_size = 7
show_board = False
pause_length = 1.0
strategy = "mcts"
c = 0.0
M = 2.0  # Max time per actual move in seconds

Strategies(board_size, show_board, strategy, c, M)

