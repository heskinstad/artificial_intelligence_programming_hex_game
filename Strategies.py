import math
import pickle
import random

import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree

class Strategies:
    def __init__(self, strategy, game_parameters, anet_parameters, topp_parameters, duel_extra_parameters, anets, path):

        self.board_size = game_parameters[0]
        self.visualize = game_parameters[1]
        self.rollouts_per_simulation = game_parameters[2]
        self.node_expansion = game_parameters[3]
        self.min_pause_length = game_parameters[4]
        self.c = game_parameters[5]

        self.save_interval = anet_parameters[0]
        self.num_epochs = anet_parameters[1]
        self.batch_size = anet_parameters[2]
        self.optimizer = anet_parameters[3]
        self.loss = anet_parameters[4]
        self.num_episodes = anet_parameters[5]
        self.learning_rate = anet_parameters[6]
        self.num_of_hidden_layers = anet_parameters[7]
        self.num_of_neurons_per_layer = anet_parameters[8]

        self.player1_id = topp_parameters[0]
        self.player2_id = topp_parameters[1]
        self.M = topp_parameters[2]
        self.topp_games_per_M = topp_parameters[3]
        self.anet_models_folder = topp_parameters[4]
        self.weights_episodes_multiplier = topp_parameters[5]

        self.path = path

        if strategy == "TOPP":
            self.topp_tournament()
        elif strategy == "TOPP_CUSTOM":
            self.topp_tournament_custom(anets)
        elif strategy == "DUEL":
            print(self.duel_2_players(duel_extra_parameters[0], duel_extra_parameters[1]))
        elif strategy == "GEN":
            self.gen_to_file()
        elif strategy == "TRAIN":
            self.train_network_on_single_batch()

    # Set two players up against each other. Who's beginning switches after every game played
    def duel_2_players(self, episode_number_p1, episode_number_p2):

        # Define players and wins
        player1 = Player(self.player1_id, "red")
        player2 = Player(self.player2_id, "blue")

        player1_wins = 0
        player2_wins = 0

        # Set up anets and load weights
        anet_player1 = ANET()
        model_player1 = anet_player1.initialize_model((self.board_size, self.board_size, 2), self.board_size**2, self.optimizer, self.loss, self.num_of_hidden_layers, self.num_of_neurons_per_layer)
        model_player1.load_weights(self.generate_filename(episode_number_p1))

        converter_p1 = tf.lite.TFLiteConverter.from_keras_model(model_player1)
        model_lite_p1 = converter_p1.convert()

        anet_player2 = ANET()
        model_player2 = anet_player2.initialize_model((self.board_size, self.board_size, 2), self.board_size**2, self.optimizer, self.loss, self.num_of_hidden_layers, self.num_of_neurons_per_layer)
        model_player2.load_weights(self.generate_filename(episode_number_p2))

        converter_p2 = tf.lite.TFLiteConverter.from_keras_model(model_player2)
        model_lite_p2 = converter_p2.convert()

        # Play topp_games_per_M number duel rounds
        for game_number in range(self.topp_games_per_M):

            # Starting player switches every game. Initialize each tree with this in mind
            if game_number % 2 == 0:
                tree = Tree(Node(State(Board(self.board_size), player1, player2, player1, player2), self.board_size ** 2))
            else:
                tree = Tree(Node(State(Board(self.board_size), player2, player1, player2, player1), self.board_size ** 2))

            # The first node is the node at the very top of the "future" tree
            current_node = tree.get_top_node()

            if self.visualize[1]:
                current_node.get_state().get_board().initialize_board_plot()

            # While the current game is not in an endstate (no winner)
            while True:
                # Choose which anet to use based on which player's turn it is
                if current_node.get_state().get_current_turn() == player1:
                    anet = model_lite_p1
                else:
                    anet = model_lite_p2

                # Update the current_node with the child_node that the anet proposes
                current_node = tree.anet_one_turn(
                    current_node,
                    anet,
                    self.visualize,
                    self.min_pause_length)

                check_win = current_node.node_check_win(True)

                # If any player win: give a point and break out of loop
                if check_win == player1:
                    player1_wins += 1
                    break
                elif check_win == player2:
                    player2_wins += 1
                    break

        if self.visualize[1]:
            plt.show()

        return [player1_wins, player2_wins]


    # Generate data to be used in a TOPP Tournament
    def topp_tournament_gen_data(self):

        player1 = Player(self.player1_id, "red")
        player2 = Player(self.player2_id, "blue")

        # Initialize random parameters (weights and biases) of ANET
        anet = ANET()
        model = anet.initialize_model((self.board_size, self.board_size, 2), self.board_size ** 2, self.optimizer, self.loss, self.num_of_hidden_layers, self.num_of_neurons_per_layer)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        model_lite = converter.convert()

        model.save_weights(self.generate_filename(0))

        # Save untrained/randomly weighted model before training begins

        # Play num_episodes number of games and train network after game
        for episode_number in range(1, self.num_episodes + 1):

            # Reset Replay Buffer at the beginning of every game
            RBUF = []

            # Starting player switches every game. Initialize each tree with this in mind
            if episode_number % 2 == 0:
                tree = Tree(Node(State(Board(self.board_size), player1, player2, player1, player2), self.board_size**2))
            else:
                tree = Tree(Node(State(Board(self.board_size), player2, player1, player2, player1), self.board_size**2))

            # Set the c value to the top node. This value will be copied to every generated node in the tree
            tree.get_top_node().set_c(self.c)

            # While not in a final state, run MCTS to generate children and corresponding data
            tree.mcts_tree_default_until_end(self.rollouts_per_simulation, RBUF, self.visualize, self.min_pause_length, self.node_expansion, model_lite)

            # Save current model if episode_number is dividable with save_interval
            if episode_number % self.save_interval == 0:
                save = True
            else:
                save = False

            # Prepare the training data
            X_train = []
            y_train = []

            minibatch = random.sample(RBUF, self.board_size*2-1)

            for boards, probabilities in minibatch:
                # Append the merged Player1 and Player2 boards to X_train
                X_train.append(boards)

                # Extract every probability element from the numerated node lists into its own list
                node_probabilities = []
                probabilities = np.reshape(probabilities, (self.board_size ** 2, 2))
                for element in probabilities:
                    node_probabilities.append(element[1])

                # Find the index of the highest probability, set this to the value 1.0, and the rest to 0.0
                # This is done because of the categorical cross entropy loss function of the network
                node_probabilities = np.array(node_probabilities)
                best = np.argmax(node_probabilities)
                for i in range(len(node_probabilities)):
                    node_probabilities[i] = 0
                node_probabilities[best] = 1.0

                # Flatten the probability data and add to y_train
                y_train.append(node_probabilities.flatten())

            # Make both numpy_arrays
            X_train = np.array(X_train)
            y_train = np.array(y_train)

            # Train model
            history = anet.train_model(model, self.num_epochs, self.batch_size, X_train, y_train, self.learning_rate)

            # Print accuracy and loss for the training session
            print("Episode " + str(episode_number) + " trained. Accuracy: " + str(history.history['accuracy'][-1]) + ". Loss: " + str(history.history['loss'][-1]))

            # Save ANET's current parameters for later use in tournament play
            if save:
                model.save_weights(self.generate_filename(episode_number))


    # topp_tournament creates the necessary data and then runs the TOPP Tournament
    def topp_tournament(self):
        # Create data
        self.topp_tournament_gen_data()

        players_score = [0] * self.M
        players = [0] * self.M

        # Every saved model will play against every other trained model between 0 and
        for i in range(self.M):
            players[i] = i * self.weights_episodes_multiplier
            for j in range(i, self.M):
                if i != j:
                    score = self.duel_2_players(i * self.weights_episodes_multiplier, j * self.weights_episodes_multiplier)

                    players_score[i] += score[0]
                    players_score[j] += score[1]

        print(players)
        print(players_score)


    # Run TOPP Tournament between pre-trained anet models
    def topp_tournament_custom(self, anets):
        players_score = [0] * len(anets)

        # Every saved model will play against every other trained model between 0 and
        for i in range(len(anets)):
            for j in range(i, len(anets)):
                if i != j:
                    score = self.duel_2_players(anets[i], anets[j])

                    players_score[i] += score[0]
                    players_score[j] += score[1]

        print(anets)
        print(players_score)


    # Generate a filename for the saved anet_model
    def generate_filename(self, episode_number):
        data_filename = str(self.board_size) + "x" + str(self.board_size) + "board_" + str(
            self.rollouts_per_simulation) + "rollouts_" + str(self.c) + "c_" + str(
            self.num_of_hidden_layers) + "layers_" + str(self.num_of_neurons_per_layer) + "neurons_" + str(
            episode_number) + "episodes.h5"

        return self.anet_models_folder + "/" + data_filename


    def get_actor(self, path):

        anet_player = ANET()
        model_player = anet_player.initialize_model((self.board_size, self.board_size, 2), self.board_size ** 2,
                                                      self.optimizer, self.loss, self.num_of_hidden_layers,
                                                      self.num_of_neurons_per_layer)
        model_player.load_weights(path)

        converter = tf.lite.TFLiteConverter.from_keras_model(model_player)
        model_lite = converter.convert()

        return model_lite


    def get_action(self, board):

        player_id = board.pop(0)

        board_this = Board(7)

        for i in range(7*7):
                board_this.board_positions[math.floor(i/7)][i%7] = board[i]

        if player_id == 1:
            player1 = Player(self.player1_id, "red")
            player2 = Player(self.player2_id, "blue")
        else:
            player2 = Player(self.player1_id, "red")
            player1 = Player(self.player2_id, "blue")

        tree = Tree(Node(State(board_this, player1, player2, player1, player2), 7 ** 2))

        return tree.anet_make_move(tree.get_top_node(), self.get_actor(self.path), self.visualize)


    def gen_to_file(self):

        player1 = Player(self.player1_id, "red")
        player2 = Player(self.player2_id, "blue")

        RBUF = []

        # Play num_episodes number of games and train network after game
        for episode_number in range(1, self.num_episodes + 1):

            # Starting player switches every game. Initialize each tree with this in mind
            if episode_number % 2 == 0:
                tree = Tree(Node(State(Board(self.board_size), player1, player2, player1, player2), self.board_size**2))
            else:
                tree = Tree(Node(State(Board(self.board_size), player2, player1, player2, player1), self.board_size**2))

            # Set the c value to the top node. This value will be copied to every generated node in the tree
            tree.get_top_node().set_c(self.c)

            # While not in a final state, run MCTS to generate children and corresponding data
            tree.mcts_tree_default_until_end(self.rollouts_per_simulation, RBUF, self.visualize, self.min_pause_length, self.node_expansion)

            # Backup
            if episode_number % 100 == 0:
                with open("bkp" + str(episode_number) + "episodes", 'wb') as f:
                    pickle.dump(RBUF, f)

            print("Episode " + str(episode_number) + " finished")

        with open("finished_" + str(self.num_episodes) + "episodes", 'wb') as f:
            pickle.dump(RBUF, f)


    def train_network_on_single_batch(self):
        # Each case (current node and children node probabilities) are stored at the end of each episode
        RBUF = []
        with open("bkp1300episodes_new", 'rb') as f:
            RBUF = pickle.load(f)

        # Randomly initialize parameters (weights and biases) of ANET
        anet = ANET()
        model = anet.initialize_model((self.board_size, self.board_size, 2), self.board_size ** 2, self.optimizer, self.loss, self.num_of_hidden_layers, self.num_of_neurons_per_layer)

        # Prepare the training data
        X_train = []
        y_train = []

        minibatch = random.sample(RBUF, len(RBUF))

        for boards, probabilities in RBUF:
            # Append the merged Player1 and Player2 boards to X_train
            X_train.append(boards)

            # Extract every probability element from the numerated node lists into its own list
            node_probabilities = []
            probabilities = np.reshape(probabilities, (self.board_size ** 2, 2))
            for element in probabilities:
                node_probabilities.append(element[1])

            # Find the index of the highest probability, set this to the value 1.0, and the rest to 0.0
            # This is done because of the categorical cross entropy loss function of the network
            node_probabilities = np.array(node_probabilities)
            best = np.argmax(node_probabilities)
            for i in range(len(node_probabilities)):
                node_probabilities[i] = 0
            node_probabilities[best] = 1.0

            # Flatten the probability data and add to y_train
            y_train.append(node_probabilities.flatten())

        # Make both numpy_arrays
        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Train model
        history = anet.train_model(model, self.num_epochs, self.batch_size, X_train, y_train, self.learning_rate)

        # Save ANET's current parameters for later use in tournament play
        model.save_weights("tete_big1300.h5")

        plt.plot(history.history['accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()