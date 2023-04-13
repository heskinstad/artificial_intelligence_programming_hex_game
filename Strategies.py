import pickle
import random
import time

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree




class Strategies:
    def __init__(self, grid_size, show_plot, game_type, c, rollouts_per_episode, min_pause_length=0.01, node_expansion=1, number_of_actual_games=1, anet_parameters=None):
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
            self.anet(c, number_of_actual_games, min_pause_length, anet_parameters)

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
        player1 = Player(1, 'black')

        tree = Tree(Node(State(Board(self.grid_size), player0, player1), self.grid_size*self.grid_size))
        tree.get_top_node().set_c(c)
        tree.mcts_tree_default_until_end(player0, player1, self.num_of_rollouts, self.show_plot, pause_length, self.node_expansion)


    def anet(self, c, number_of_actual_games, pause_length, anet_parameters):

        history = None
        player0 = Player(1, 'red')
        player1 = Player(2, 'blue')


        i_s = anet_parameters[0]  # Save interval for ANET parameters
        num_epochs = anet_parameters[1]
        batch_size = anet_parameters[2]
        optimizer = anet_parameters[3]
        loss = anet_parameters[4]
        num_episodes = anet_parameters[5]

        # Each case (current node and children node probabilities) are stored at the end of each episode
        RBUF = []
        with open('playersmall', 'rb') as f:
            RBUF = pickle.load(f)

        # Randomly initialize parameters (weights and biases) of ANET
        input_shape = anet_parameters[6]
        num_of_actions = self.grid_size * self.grid_size
        anet = ANET()
        model = anet.initialize_model(input_shape, num_of_actions)

        #For g_a in number_of_actual_games
        for g_a in range(number_of_actual_games):
            #model.load_weights('anet_weights_densse_250.h5')
            # Initialize the actual game board to an empty board
            # Initialize the Monte Carlo Tree to a single root
            #tree = Tree(Node(State(Board(self.grid_size), player0, player1), self.grid_size * self.grid_size))
            #tree.get_top_node().set_c(c)
            # While not in a final state
            #tree.mcts_tree_default_until_end3(player0, player1, self.num_of_rollouts, RBUF, self.show_plot, pause_length, self.node_expansion, model)


            # Remove every turn of one of the players from RBUF
            '''for i in RBUF:
                if i[0][1] == 1:
                    i.clear()
            RBUF = [empty for empty in RBUF if empty]'''

            minibatch = random.sample(RBUF, num_episodes)
            X_train = []
            y_train = []

            print(RBUF)

            for root, D in minibatch:
                board = root[0]
                board = np.append(board, root[1])

                X_train.append(board)

                # Extract every normalized probability element from the numerated node lists into its own list
                node_probabilities = []
                for e in D:
                    node_probabilities.append(e[1])
                y_train.append(node_probabilities)

            X_train = np.array(X_train)
            y_train = np.asarray(y_train)

            if g_a == i_s:

                history = anet.train_model(model, num_epochs, batch_size, optimizer, loss, X_train, y_train)

                # Save ANET's current parameters for later use in tournament play
                model.save_weights('anet_weights_dense_small_' + str(250) + '.h5')
                #with open('playersmall','wb') as f:
                #    pickle.dump(RBUF, f)

        plt.plot(history.history['accuracy'])
        #plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        #plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()