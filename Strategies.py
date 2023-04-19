import matplotlib.pyplot as plt
import numpy as np

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree


class Strategies:
    def __init__(self, game_parameters, anet_parameters, topp_parameters):

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

        self.player1_id = topp_parameters[0]
        self.player2_id = topp_parameters[1]
        self.M = topp_parameters[2]
        self.topp_games_per_M = topp_parameters[3]
        self.anet_models_folder = topp_parameters[4]
        self.weights_episodes_multiplier = topp_parameters[5]


        self.topp_tournament()


    def topp_tournament_2_players(self, episode_number_p1, episode_number_p2):

        player1 = Player(self.player1_id, "red")
        player2 = Player(self.player2_id, "blue")

        player1_wins = 0
        player2_wins = 0

        anet_player1 = ANET()
        model_player1 = anet_player1.initialize_model((self.board_size, self.board_size, 2), self.board_size**2, self.optimizer, self.loss)
        model_player1.load_weights(self.generate_filename(episode_number_p1))

        anet_player2 = ANET()
        model_player2 = anet_player2.initialize_model((self.board_size, self.board_size, 2), self.board_size**2, self.optimizer, self.loss)
        model_player2.load_weights(self.generate_filename(episode_number_p2))

        for game_number in range(self.topp_games_per_M):

            # Starting player switches each game
            if game_number % 2 == 0:
                tree = Tree(Node(State(Board(self.board_size), player1, player2, player1, player2), self.board_size ** 2))
            else:
                tree = Tree(Node(State(Board(self.board_size), player2, player1, player2, player1), self.board_size ** 2))

            current_node = tree.get_top_node()

            while True:
                if current_node.get_state().get_current_turn() == player1:
                    anet = model_player1
                else:
                    anet = model_player2

                current_node = tree.anet_one_turn(
                    current_node,
                    anet,
                    self.visualize,
                    self.min_pause_length)

                check_win = current_node.node_check_win(True)

                #current_node.get_state().get_board().print_board()

                if check_win == player1:
                    player1_wins += 1
                    break
                elif check_win == player2:
                    player2_wins += 1
                    break

        #print("Player 1 won " + str(player1_wins) + " times")
        #print("Player 2 won " + str(player2_wins) + " times")

        if self.visualize[1]:
            plt.show()

        return [player1_wins, player2_wins]


    def generate_filename(self, episode_number):
        data_filename = str(self.board_size) + "x" + str(self.board_size) + "board_" + str(
            self.rollouts_per_simulation) + "rollouts_" + str(self.c) + "c_" + str(episode_number) + "episodes.h5"

        return self.anet_models_folder + "/" + data_filename


    def topp_tournament_gen_data(self):

        player1 = Player(self.player1_id, "red")
        player2 = Player(self.player2_id, "blue")

        # Randomly initialize parameters (weights and biases) of ANET
        anet = ANET()
        model = anet.initialize_model((self.board_size, self.board_size, 2), self.board_size ** 2, self.optimizer, self.loss)

        model.save_weights(self.generate_filename(0))  # Save untrained model before training begins

        for episode_number in range(1, self.num_episodes + 1):

            RBUF = []

            if episode_number % 2 == 0:
                tree = Tree(Node(State(Board(self.board_size), player1, player2, player1, player2), self.board_size**2))
            else:
                tree = Tree(Node(State(Board(self.board_size), player2, player1, player2, player1), self.board_size**2))

            tree.get_top_node().set_c(self.c)
            # While not in a final state
            tree.mcts_tree_default_until_end(self.rollouts_per_simulation, RBUF, self.visualize, self.min_pause_length, self.node_expansion, model)

            if episode_number % self.save_interval == 0:
                save = True
            else:
                save = False

            X_train = []
            y_train = []

            for root, D in RBUF:
                X_train.append(root)

                # Extract every normalized probability element from the numerated node lists into its own list
                node_probabilities = []
                new = np.reshape(D, (self.board_size ** 2, 2))
                for e in new:
                    node_probabilities.append(e[1])
                node_probabilities = node_probabilities / np.sum(node_probabilities)  # Normalize probabilites
                best = np.argmax(node_probabilities)
                for i in range(len(node_probabilities)):
                    node_probabilities[i] = 0
                node_probabilities[best] = 1.0

                y_train.append(node_probabilities.flatten())

            X_train = np.array(X_train)
            y_train = np.asarray(y_train)

            history = anet.train_model(model, self.num_epochs, self.batch_size, X_train, y_train, self.learning_rate)

            print("Episode " + str(episode_number) + " trained. Accuracy: " + str(history.history['accuracy'][-1]) + ". Loss: " + str(history.history['loss'][-1]))

            # Save ANET's current parameters for later use in tournament play
            if save:
                model.save_weights(self.generate_filename(episode_number))


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
                    score = self.topp_tournament_2_players(i * self.weights_episodes_multiplier, j * self.weights_episodes_multiplier)

                    players_score[i] += score[0]
                    players_score[j] += score[1]

        print(players)
        print(players_score)