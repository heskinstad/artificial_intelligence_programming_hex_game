from Board import Board
from Node import Node
from Player import Player
from State import State
from Strategies import Strategies
from Tree import Tree

board_size = 11
show_board = True

game = Strategies(board_size, show_board)

game.place_randomly()

player0 = Player(0, 'red')
player1 = Player(1, 'blue')

#tree = Tree(Node(State(Board(board_size, show_board), player0, player1)))
#tree.get_top_node().create_child_nodes_for_player(player0, player1, 3)
#tree.get_top_node().get_children()[0].get_children()[0].get_children()[0].get_state().get_board().print_board()
#tree.print_all_nodes_as_boards()


#tree = Tree(Node(State(Board(board_size, show_board), player0, player1)))
#tree.simulate_all(player0, player1)
#print(tree.get_top_node().get_score())