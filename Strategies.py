import pickle
import random
import time

import matplotlib.pyplot as plt
import numpy as np

from ANET import ANET
from Board import Board
from Node import Node
from Player import Player
from State import State
from Tree import Tree


class Strategies:
    def __init__(self, game_type, game_parameters, anet_parameters, topp_parameters):

        board_size = game_parameters[0]
        show_plot = game_parameters[1]
        rollouts_per_episode = game_parameters[2]
        node_expansion = game_parameters[3]
        min_pause_length = game_parameters[4]
        c = game_parameters[5]
        number_of_actual_games = game_parameters[6]
        data_filename = game_parameters[7]

        save_interval = anet_parameters[0]
        num_epochs = anet_parameters[1]
        batch_size = anet_parameters[2]
        optimizer = anet_parameters[3]
        loss = anet_parameters[4]
        num_episodes = anet_parameters[5]
        weights_filename = anet_parameters[6]
        learning_rate = anet_parameters[7]

        player1 = topp_parameters[0]
        player2 = topp_parameters[1]
        player1_weights_loc = topp_parameters[2]
        player2_weights_loc = topp_parameters[3]
        number_of_topp_games = topp_parameters[4]
        save_folder = topp_parameters[5]
        topp_mini_games = topp_parameters[6]

        if game_type == "random":
            self.place_randomly(board_size, show_plot, min_pause_length)
        elif game_type == "mcts":
            self.mcts(board_size, c, rollouts_per_episode, node_expansion, min_pause_length, show_plot)
        elif game_type == "generate_data":
            self.generate_data(board_size, c, number_of_actual_games, rollouts_per_episode, node_expansion, min_pause_length, show_plot, data_filename)
        elif game_type == "train_network":
            self.train_network(board_size, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, data_filename, learning_rate)
        elif game_type == "train_networks":
            self.train_networks(board_size, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, data_filename, save_interval, learning_rate)
        elif game_type == "topp_tournament_2_players":
            self.topp_tournament_2_players(player1, player2, player1_weights_loc, player2_weights_loc, board_size, number_of_topp_games, show_plot, min_pause_length)
        elif game_type == "topp_tournament":
            self.topp_tournament(player1, player2, board_size, number_of_topp_games, show_plot, min_pause_length, save_interval, num_epochs, batch_size, optimizer, loss, learning_rate, rollouts_per_episode, node_expansion, c, save_folder)
        elif game_type == "topp_mini":
            self.TOPP_mini(player1, player2, board_size, number_of_topp_games, show_plot, min_pause_length, save_interval, num_epochs, batch_size, optimizer, loss, learning_rate, rollouts_per_episode, node_expansion, c, save_folder, topp_mini_games)

    def place_randomly(self, board_size, show_plot, pause_length):
        gameBoard = Board(board_size)

        if show_plot:
            gameBoard.initialize_board_plot()

        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        i = -1
        while i < board_size * board_size - 1:
            pause_start = time.time()

            random_x = int(random.uniform(0, board_size))
            random_y = int(random.uniform(0, board_size))

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

            if show_plot:
                gameBoard.create_board_plot(gameBoard.get_fig(), gameBoard.get_ax())
                if time.time() > pause_start + pause_length:
                    plt.pause(time.time() - pause_start + pause_length)

        gameBoard.print_board()

        if show_plot:
            gameBoard.create_board_plot(gameBoard.get_fig(), gameBoard.get_ax())
            plt.show()


    def mcts(self, board_size, c, rollouts_per_episode, node_expansion, pause_length, show_plot):
        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        tree = Tree(Node(State(Board(board_size), player0, player1, player0, player1), board_size**2))
        tree.get_top_node().set_c(c)
        tree.mcts_tree_default_until_end(rollouts_per_episode, show_plot, pause_length, node_expansion)


    def generate_data(self, board_size, c, number_of_actual_games, rollouts_per_episode, node_expansion, min_pause_length, show_plot, filename):

        player0 = Player(1, 'red')
        player1 = Player(2, 'blue')

        # Each case (current board and children node probabilities) are stored at the end of each episode
        RBUF = []

        #TODO: Edit training board input so that if it's player1's turn the board will be filled with 0's, 1's and 2's
        # and if it's player2's turn the board will be filled with 3's, 4's and 5's.
        # Also then get rid of the 1/2 at the end of every board.
        # Remember to implement this when it uses the ANET while playing too, not just in training.

        anet_player1 = ANET()
        model_player1 = anet_player1.initialize_model((board_size, board_size, 1), board_size ** 2)
        model_player1.load_weights("weights/tete.h5")

        for g_a in range(number_of_actual_games):
            # Initialize the actual game board to an empty board
            # Initialize the Monte Carlo Tree to a single root
            tree = Tree(Node(State(Board(board_size), player0, player1, player0, player1), board_size**2))
            tree.get_top_node().set_c(c)
            # While not in a final state
            tree.mcts_tree_default_until_end(rollouts_per_episode, show_plot, min_pause_length, node_expansion)

        with open(filename, 'wb') as f:
            pickle.dump(RBUF, f)


    def train_network(self, board_size, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, data_filename, learning_rate, save=False, RBUF=None, anet=None):

        # Each case (current node and children node probabilities) are stored at the end of each episode
        if RBUF == None:
            RBUF = []
            with open(data_filename, 'rb') as f:
                RBUF = pickle.load(f)


        # Randomly initialize parameters (weights and biases) of ANET
        input_shape = (board_size, board_size, 1)
        num_of_actions = board_size**2
        if anet == None:
            anet = ANET()
            model = anet.initialize_model(input_shape, num_of_actions)

        #TODO: Edit training board input so that if it's player1's turn the board will be filled with 0's, 1's and 2's
        # and if it's player2's turn the board will be filled with 3's, 4's and 5's.
        # Also then get rid of the 1/2 at the end of every board.
        # Remember to implement this when it uses the ANET while playing too, not just in training.

        if num_episodes > 0:  # If there are no episodes skip the training

            X_train = []
            y_train = []

            for root, D in RBUF:
                X_train.append(root)
                print(root)

                # Extract every normalized probability element from the numerated node lists into its own list
                node_probabilities = []
                for e in D:
                    node_probabilities.append(e[1])

                node_probabilities = node_probabilities / np.sum(node_probabilities)  # Normalize probabilites
                y_train.append(node_probabilities)


            X_train = np.array(X_train)
            y_train = np.asarray(y_train)

            history = anet.train_model(model, num_epochs, batch_size, optimizer, loss, X_train, y_train, learning_rate)

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

        # Save ANET's current parameters for later use in tournament play
        if save:
            model.save_weights(weights_filename)
        return model



    def train_networks(self, board_size, num_epochs, batch_size, optimizer, loss, num_episodes, weights_filename, data_filename, save_interval, learning_rate):

        for i in range(num_episodes+1):
            if i % save_interval:
                self.train_network(board_size, num_epochs, batch_size, optimizer, loss, i, weights_filename, data_filename, learning_rate)


    def topp_tournament_2_players(self, player1, player2, player1_weights_loc, player2_weights_loc, board_size, number_of_topp_games, show_plot, min_pause_length):

        player1 = Player(player1, "red", "horizontal")
        player2 = Player(player2, "blue", "vertical")

        player1_wins = 0
        player2_wins = 0

        anet_player1 = ANET()
        model_player1 = anet_player1.initialize_model((board_size, board_size, 1), board_size**2)
        model_player1.load_weights(player1_weights_loc)

        anet_player2 = ANET()
        model_player2 = anet_player2.initialize_model((board_size, board_size, 1), board_size**2)
        model_player2.load_weights(player2_weights_loc)

        for game_number in range(number_of_topp_games):

            # Starting player switches each game
            if game_number % 2 == 0:
                tree = Tree(Node(State(Board(board_size), player1, player2, player1, player2), board_size ** 2))
            else:
                tree = Tree(Node(State(Board(board_size), player2, player1, player2, player1), board_size ** 2))

            current_node = tree.get_top_node()

            while True:
                if current_node.get_state().get_current_turn() == player1:
                    anet = model_player1
                else:
                    anet = model_player2

                current_node = tree.anet_one_turn(
                    current_node,
                    anet,
                    show_plot,
                    min_pause_length)

                check_win = current_node.node_check_win(True)

                if check_win == player1:
                    player1_wins += 1
                    break
                elif check_win == player2:
                    player2_wins += 1
                    break

        #print("Player 1 won " + str(player1_wins) + " times")
        #print("Player 2 won " + str(player2_wins) + " times")

        if show_plot:
            plt.show()

        return [player1_wins, player2_wins]



    def topp_tournament(self, player1, player2, board_size, number_of_topp_games, show_plot, min_pause_length, save_interval, num_epochs, batch_size, optimizer, loss, learning_rate, rollouts_per_episode, node_expansion, c, save_folder):

        player1 = Player(player1, "red")
        player2 = Player(player2, "blue")

        # Randomly initialize parameters (weights and biases) of ANET
        input_shape = (board_size, board_size, 1)
        num_of_actions = board_size ** 2
        anet = ANET()
        model = anet.initialize_model(input_shape, num_of_actions)
        #model.load_weights((save_folder) + "/TOPP_970.h5")

        model.save_weights(str(save_folder) + "/TOPP_0.h5")



        for game_number in range(1, number_of_topp_games + 1):

            RBUF = []


            if game_number % 2 == 0:
                tree = Tree(Node(State(Board(board_size), player1, player2, player1, player2), board_size**2))
            else:
                tree = Tree(Node(State(Board(board_size), player2, player1, player2, player1), board_size**2))

            tree.get_top_node().set_c(c)
            # While not in a final state
            tree.mcts_tree_default_until_end3(rollouts_per_episode, RBUF, show_plot, min_pause_length, node_expansion, model)

            if game_number % save_interval == 0:
                save = True
            else:
                save = False

            X_train = []
            y_train = []

            for root, D in RBUF:
                X_train.append(root)

                # Extract every normalized probability element from the numerated node lists into its own list
                node_probabilities = []
                for e in D:
                    node_probabilities.append(e[1])
                node_probabilities = node_probabilities / np.sum(node_probabilities)  # Normalize probabilites

                best = np.argmax(node_probabilities)
                for i in range(len(node_probabilities)):
                    node_probabilities[i] = 0
                node_probabilities[best] = 1.0

                y_train.append(node_probabilities)

            X_train = np.array(X_train)
            y_train = np.asarray(y_train)

            history = anet.train_model(model, num_epochs, batch_size, optimizer, loss, X_train, y_train, learning_rate)

            print("Episode " + str(game_number) + " trained. Accuracy: " + str(history.history['accuracy'][-1]) + ". Loss: " + str(history.history['loss'][-1]))

            # Save ANET's current parameters for later use in tournament play
            if save:
                model.save_weights(str(save_folder) + "/TOPP_" + str(game_number) + ".h5")

    def TOPP_mini(self, player1, player2, board_size, number_of_topp_games, show_plot, min_pause_length, save_interval, num_epochs, batch_size, optimizer, loss, learning_rate, rollouts_per_episode, node_expansion, c, save_folder, topp_mini_games):
        # Create data
        self.topp_tournament(player1, player2, board_size, number_of_topp_games, show_plot, min_pause_length, save_interval, num_epochs, batch_size, optimizer, loss, learning_rate, rollouts_per_episode, node_expansion, c, save_folder)

        players_score = [0, 0, 0, 0, 0, 0]

        for i in range(0, len(players_score)):
            for j in range(i, len(players_score)):
                if i != j:
                    score = self.topp_tournament_2_players(player1, player2, save_folder + "/TOPP_" + str(i*20) + ".h5", save_folder + "/TOPP_" + str(j*20) + ".h5", board_size, topp_mini_games, show_plot, min_pause_length)

                    players_score[i] += score[0]
                    players_score[j] += score[1]

        print(players_score)