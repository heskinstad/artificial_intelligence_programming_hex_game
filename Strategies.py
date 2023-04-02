import random
import time

import matplotlib.pyplot as plt

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree


class Strategies:
    def __init__(self, grid_size, show_plot, game_type, c, rollouts_per_episode, min_pause_length=0.01, node_expansion=1, number_of_actual_games=1):
        self.grid_size = grid_size
        self.show_plot = show_plot
        self.game_type = game_type
        self.num_of_rollouts = rollouts_per_episode
        self.node_expansion = node_expansion

        if game_type == "random":
            self.place_randomly(min_pause_length)
        elif game_type == "mcts":
            self.mcts(c, min_pause_length)
        elif game_type == "anet":
            self.anet(number_of_actual_games)

    def place_randomly(self, pause_length):
        gameBoard = Board(self.grid_size)

        if self.show_plot:
            gameBoard.initialize_board_plot()

        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        i = -1
        while i < self.grid_size * self.grid_size - 1:
            pause_start = time.time()

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
                if time.time() > pause_start + pause_length:
                    plt.pause(time.time() - pause_start + pause_length)

        gameBoard.print_board()

        if self.show_plot:
            gameBoard.create_board_plot(gameBoard.get_fig(), gameBoard.get_ax())
            plt.show()

    def mcts(self, c, pause_length):
        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        tree = Tree(Node(State(Board(self.grid_size), player0, player1), self.grid_size*self.grid_size))
        tree.get_top_node().set_c(c)
        tree.mcts_tree_default_until_end(player0, player1, self.num_of_rollouts, self.show_plot, pause_length, self.node_expansion)


    def anet(self, number_of_actual_games):

        i_s = 1000  # Save interval for ANET parameters

        RBUF = []  # Clear Replay Buffer

        # Randomly initialize parameters (weights and biases) of ANET
        input_shape = (7, 7, 2)
        num_of_actions = 7 * 7
        anet = ANET(input_shape, num_of_actions)

