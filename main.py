from Strategies import Strategies

board_size = 4
show_board = False
pause_length = 1.0
strategy = "mcts"
c = 1.0
M = 20.0  # Max time per actual move in seconds

Strategies(board_size, show_board, strategy, c, M)




