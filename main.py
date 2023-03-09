from Strategies import Strategies

board_size = 6
show_board = True
pause_length = 1.0
strategy = "mcts"
c = 1
M = 20.0  # Max time per actual move in seconds

Strategies(board_size, show_board, strategy, c, M)




