import pickle
import random
import time

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree

from sklearn.model_selection import train_test_split


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

        # Each case (current node and children node probabilities) are stored at the end of each episode
        RBUF = []
        with open('tete', 'rb') as f:
            RBUF = pickle.load(f)

        # Randomly initialize parameters (weights and biases) of ANET
        input_shape = (self.grid_size, self.grid_size, 1)
        num_of_actions = self.grid_size * self.grid_size
        #anet = ANET(input_shape, num_of_actions)
        anet = keras.models.Sequential()

        anet.add(
            keras.layers.InputLayer(
                input_shape=input_shape
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (3, 3),
                activation='relu',
                padding='same',
                kernel_regularizer=keras.regularizers.l2()
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (3, 3),
                activation='relu',
                padding='same',
                kernel_regularizer=keras.regularizers.l2()
            )
        )

        anet.add(
            keras.layers.Flatten()
        )

        anet.add(
            keras.layers.Dense(
            num_of_actions,
            activation='softmax'
            )
        )

        # Add convolutional layers to extract features from the input
        '''anet.add(keras.layers.Conv2D(64, kernel_size=2, activation='relu', input_shape=input_shape))
        anet.add(keras.layers.Conv2D(32, kernel_size=2, activation='relu'))

        # Flatten the output of the convolutional layers
        anet.add(keras.layers.Flatten())

        # Add fully connected layers to predict the probability of good child states
        anet.add(keras.layers.Dense(128, activation='relu'))
        anet.add(keras.layers.Dense(64, activation='relu'))
        anet.add(keras.layers.Dense(49, activation='softmax'))'''

        '''anet.add(tf.keras.layers.Conv2D(49, (3, 3), activation='relu', padding='same', input_shape=input_shape))
        anet.add(tf.keras.layers.Conv2D(49, (3, 3), activation='relu', padding='same'))
        anet.add(tf.keras.layers.Conv2D(49, (3, 3), activation='relu', padding='same'))
        anet.add(tf.keras.layers.Flatten())
        anet.add(tf.keras.layers.Dense(49, activation='relu'))
        anet.add(tf.keras.layers.Dropout(0.5))
        anet.add(tf.keras.layers.Dense(num_of_actions, activation='softmax'))'''

        #For g_a in number_of_actual_games
        for g_a in range(number_of_actual_games):
            #anet.load_weights('anet_weights_15.h5')
            # Initialize the actual game board to an empty board
            # Initialize the Monte Carlo Tree to a single root
            '''tree = Tree(Node(State(Board(self.grid_size), player0, player1), self.grid_size * self.grid_size))
            tree.get_top_node().set_c(c)
            # While not in a final state
            tree.mcts_tree_default_until_end3(player0, player1, self.num_of_rollouts, RBUF, self.show_plot, pause_length, self.node_expansion, anet)
'''
            #TODO: train ANET on a random minibatch of cases from RBUF
            minibatch = random.sample(RBUF, 14*g_a+1)
            #train, val = train_test_split(RBUF, test_size=0.2, random_state=42)
            X_train = []
            y_train = []
            for root, D in minibatch:

                # Extract every normalized probability element from the numerated node lists into its own list
                node_probabilities = []
                for e in D:
                    node_probabilities.append(e[1])

                X_train.append(root.get_state().get_board().get_board_np())
                y_train.append(node_probabilities)

            X_train = np.array(X_train)
            y_train = np.asarray(y_train)

            if g_a % i_s == 0:

                anet.compile(
                    optimizer=optimizer,
                    loss=loss,
                    metrics=['accuracy']
                )
                from keras import backend as K
                K.set_value(anet.optimizer.learning_rate, 0.01)
                history = anet.fit(
                    X_train,
                    y_train,
                    batch_size=batch_size,
                    epochs=num_epochs,
                    verbose=1
                )

                '''X_test = []
                y_test = []
                for root, D in val:

                    node_probabilities = []
                    for e in D:
                        node_probabilities.append(e[1])

                    X_test.append(root.get_state().get_board().get_board_np())
                    y_test.append(node_probabilities)

                X_test = np.array(X_test)
                y_test = np.asarray(y_test)

                losss, accuracy = anet.evaluate(
                    X_test,
                    y_test
                )

                # Print the loss and accuracy
                print(f'\nTest loss: {losss:.6f}')
                print(f'Test accuracy: {accuracy * 100:.2f}%')'''

                # Save ANET's current parameters for later use in tournament play
                anet.save_weights('anet_weights_' + str(g_a) + '.h5')
                #with open('tete','wb') as f:
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