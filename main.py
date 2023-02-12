from Board import Board
from Node import Node
from Player import Player
from State import State
from Strategies import Strategies
from Tree import Tree

board_size = 4
show_board = False

#game = Strategies(board_size, show_board)

#game.place_randomly()

player0 = Player(0, 'red')
player1 = Player(1, 'blue')

tree = Tree(Node(State(Board(board_size, show_board), player0, player1)))
tree.get_top_node().get_state().get_board().place(player0, 2, 2)
tree.get_top_node().get_state().get_board().place(player1, 2, 3)
tree.get_top_node().get_state().get_board().place(player0, 3, 0)
tree.get_top_node().get_state().get_board().place(player1, 1, 3)
tree.get_top_node().create_child_nodes_for_player(player0)
tree.print_all_nodes_as_boards()