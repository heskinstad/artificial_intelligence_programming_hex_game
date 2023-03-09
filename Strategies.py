import random
import matplotlib.pyplot as plt

from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree


class Strategies:
    def __init__(self, grid_size, show_plot, game_type, c, max_time=9999, pause_length=0.01):
        self.grid_size = grid_size
        self.show_plot = show_plot
        self.game_type = game_type
        self.max_time = max_time

        if game_type == "random":
            self.place_randomly(pause_length)
        elif game_type == "mcts":
            self.mcts(c, pause_length)

    def place_randomly(self, pause_length):
        gameBoard = Board(self.grid_size)

        if self.show_plot:
            gameBoard.initialize_board_plot()

        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        i = -1
        while i < self.grid_size * self.grid_size - 1:
            random_x = int(random.uniform(0, self.grid_size))
            random_y = int(random.uniform(0, self.grid_size))

            if gameBoard.get_hex_by_x_y(random_x, random_y) != None:
                continue

            if i % 2:
                gameBoard.place(player0, random_x, random_y)
                if gameBoard.check_if_player_won(player0) == player0:
                    print('Game ended: ' + player0.get_color() + ' won!')
                    break
            else:
                gameBoard.place(player1, random_x, random_y)
                if gameBoard.check_if_player_won(player1) == player1:
                    print('Game ended: ' + player1.get_color() + ' won!')
                    break

            i += 1

            if self.show_plot:
                gameBoard.create_board_plot(gameBoard.get_fig(), gameBoard.get_ax())
                plt.pause(pause_length)

        gameBoard.print_board()

        if self.show_plot:
            gameBoard.create_board_plot(gameBoard.get_fig(), gameBoard.get_ax())
            plt.show()

    def mcts(self, c, pause_length):
        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        tree = Tree(Node(State(Board(self.grid_size), player0, player1)))
        tree.get_top_node().set_c(c)
        tree.mcts_tree_default_until_end(player0, player1, 2, self.max_time, self.show_plot, pause_length)