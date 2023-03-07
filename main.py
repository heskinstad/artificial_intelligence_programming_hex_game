import time

from Board import Board
from Node import Node
from Player import Player
from State import State
from Strategies import Strategies
from Tree import Tree

board_size = 4
show_board = True
pause_length = 1.0
strategy = "mcts"

Strategies(board_size, show_board, strategy)




