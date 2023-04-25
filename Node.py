import copy
import math
import random

import numpy as np
import tensorflow as tf

from Board import Board
from State import State
from Exceptions.IllegalNumberOfChildrenException import IllegalNumberOfChildrenException

# The Node class keep info about the individual nodes that make up a tree
class Node:
    def __init__(self, state, max_children, parent=None, score=None, endstate=False):
        if score is None:
            score = [0, 0]
        self.state = state
        self.parent = parent
        self.children = []
        self.score = score  # Holds the accumulated [number_of_visits, score]
        self.endstate = endstate
        self.c = None
        self.leaf = False
        self.top_node = False
        self.max_children = max_children
        self.node_num = None

    def get_state(self):
        return self.state

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def set_c(self, c):
        self.c = c

    def get_c(self):
        return self.c

    def is_endstate(self):
        return self.endstate

    def make_endstate(self):
        self.endstate = True

    def is_leaf(self):
        return self.leaf

    def set_leaf_status(self):
        self.leaf = True

    def remove_leaf_status(self):
        self.leaf = False

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)

    def remove_all_children(self):
        self.children = []

    def set_as_top_node(self):
        self.top_node = True

    def is_top_node(self):
        return self.top_node

    def get_max_children(self):
        return self.max_children

    def set_node_num(self, node_num):
        self.node_num = node_num

    def get_node_num(self):
        return self.node_num


    # Create a single, randomized child node, unless a position argument is included
    def create_random_child_node(self, position=None):
        board = self.get_state().get_board()

        # Create a 'board' with coordinates
        positions = []
        for y in range(board.get_board_size()):
            for x in range(board.get_board_size()):
                positions.append([y, x])

        while len(positions) > 0:

            # Select x and y randomly from the available positions
            index = int(random.uniform(0, len(positions)))
            x = positions[index][1]
            y = positions[index][0]

            if position != None:
                x = position[1]
                y = position[0]

            # Check if it already exists in any of the other children nodes
            in_current_child = False
            if len(self.get_children()) > 0:
                for child in self.get_children():
                    if child.get_state().get_board().get_hex_by_x_y(x, y) != 0:
                        in_current_child = True

            if board.get_hex_by_x_y(x, y) == 0 and not in_current_child:
                return self.create_child_node([y, x])

            # If the space is occupied, delete the position from the array and try again
            else:
                del positions[index]

        # Return None if there are no free spaces left
        return None


    def create_child_node(self, position):
        x = position[1]
        y = position[0]

        board = self.get_state().get_board()

        board_deepcopy = Board(board.get_board_size(), False)
        board_deepcopy.board_positions = [x[:] for x in board.get_board_p1()]

        board_deepcopy.place(self.get_state().get_current_turn(), x, y)

        child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()),
                     self.get_max_children() - 1, self)
        child.c = self.get_c()
        child.set_node_num(y * board.get_board_size() + x)

        self.add_child(child)

        return child

    ####################
    # POLICY FUNCTIONS #
    ####################

    '''
    Tree policy:
    Choose the branch with the highest combination of exploitation + exploration
    Q(s, a) + u(s, a)
    where
    Q(s, a) is the value of the final expected result of doing action a from node s (updated after each rollout)
    - can be considered the score of a child node
    and
    u(s, a) is the exploration bonus
    '''

    # Tree policy. Traverses already existing nodes and can create new leaf nodes
    def mcts_tree_policy(self, node_expansion, anet):
        # If self is an endstate, then propagate the score and return because there are no possible child states
        score = self.node_check_win()
        if self.is_endstate():
            self.propagate_score(score)
            return

        # Expand with default policy if:
        # Node is leaf or
        # The current number of nodes on this level is less than half of the maximum number of nodes on this level
        elif self.is_leaf() or len(self.get_children()) < (self.get_max_children() - 1) / node_expansion:
            self.set_leaf_status()
            self.mcts_default_policy(anet)
            self.remove_leaf_status()
        else:
            best_child = self.calc_best_child()
            best_child.mcts_default_policy(anet)


    # A run of the default policy is one rollout
    def mcts_default_policy(self, anet):
        score = self.node_check_win()

        # If anyone won in this node
        if self.is_endstate():
            self.propagate_score(score)
            return

        action_probs = self.get_anet_position_prediction(anet)



        child_node = None
        #if self.get_max_children() == len(self.get_children()):
        #    child_node = random.choice(self.get_children())

        while child_node == None:

            # Make sure there are no nan's in the prediction, the network sometimes outputs no legal
            if np.isnan(action_probs[5]) or np.isnan(action_probs[2]):
                return
            action_probs = action_probs / np.sum(action_probs)

            # Choose move with highest probability
            #action_idx = np.argmax(action_probs)
            if np.isnan(action_probs[5]) or np.isnan(action_probs[2]):
                action_idx = np.random.choice(len(action_probs), p=self.get_valid_moves().flatten() / np.sum(self.get_valid_moves().flatten()))
            else:
                action_idx = np.random.choice(len(action_probs), p=action_probs)

            # Convert position to 2D coordinates
            position = [None, None]
            position[0] = math.floor(action_idx / self.get_state().get_board().get_board_size())
            position[1] = action_idx % self.get_state().get_board().get_board_size()

            child_node = self.create_random_child_node(position)

            action_probs[action_idx] = 0.0

        child_node.mcts_default_policy(anet)

        # If top node in the newly generated default policy tree
        # Remove own children and set itself as a leaf
        if self.get_parent() != None:
            if self.get_parent().is_leaf():
                self.remove_all_children()
                self.set_leaf_status()
        else:
            return


    # Sends the current state of the board to the anet and returns the position of the predicted best next move
    def anet_policy(self, anet):
        # Convert board to anet-readable format
        action_probs = self.get_anet_position_prediction(anet)

        # Add a mask (valid_moves) to give all 'illegal' moves a probability of zero
        valid_moves = self.get_valid_moves().flatten()
        action_probs = action_probs * valid_moves
        action_probs = action_probs / np.sum(action_probs)
        action_probs = np.array(action_probs)
        action_probs = action_probs / np.sum(action_probs)

        # If the network produces no possible moves, choose a random, valid move
        if np.isnan(action_probs[5]) or np.isnan(action_probs[2]):
            action_idx = np.random.choice(len(action_probs), p=self.get_valid_moves().flatten() / np.sum(self.get_valid_moves().flatten()))
        else:
            for i in range(len(action_probs)):
                action_probs[i] = action_probs[i]**2
            action_probs = action_probs / np.sum(action_probs)
            action_idx = np.random.choice(len(action_probs), p=action_probs)

        return action_idx

    # Return an array of valid moves. Dimensions same as game board where 0 = occupied and 1 = free
    def get_valid_moves(self):
        valid_moves = copy.deepcopy(self.get_state().get_board().get_board_np())
        for y in range(len(valid_moves)):
            for x in range(len(valid_moves[y])):
                if valid_moves[y][x] == 0:
                    valid_moves[y][x] = 1
                else:
                    valid_moves[y][x] = 0

        return valid_moves


    #####################################
    # CHECK WIN AND PROPAGATE FUNCTIONS #
    #####################################

    # Propagates the score given as a parameter to the node self and every parent up throughout the tree
    def propagate_score(self, score):
        current_node = self

        # Go up to every parent and add score until there are no parents
        while current_node.get_parent() != None:
            current_node.set_score([current_node.get_score()[0] + score[0], current_node.get_score()[1] + score[1]])
            current_node = current_node.get_parent()

        current_node.set_score([current_node.get_score()[0] + score[0], current_node.get_score()[1] + score[1]])


    def node_check_win(self, return_player=False):

        current_player = self.get_state().get_current_turn()
        next_turn_player = self.get_state().get_next_turn()
        starting_player = self.get_state().get_starting_player()
        second_player = self.get_state().get_second_player()

        # If player won this simulation
        if self.get_state().get_board().check_if_player_won(current_player, starting_player, second_player) == starting_player\
             or self.get_state().get_board().check_if_player_won(next_turn_player, starting_player, second_player) == starting_player:
            self.make_endstate()
            if return_player:
                return self.get_state().get_starting_player()
            return [1, 1]

        # If player lost this simulation
        elif self.get_state().get_board().check_if_player_won(current_player, starting_player, second_player) == second_player\
             or self.get_state().get_board().check_if_player_won(next_turn_player, starting_player, second_player) == second_player:
            self.make_endstate()
            if return_player:
                return self.get_state().get_second_player()
            return [1, -1]

        # If no one won
        else:
            return 0


    #########################################
    # RETURN MOST PROMISING CHILD FUNCTIONS #
    #########################################

    # Return the child with the best score relative to the current player
    def calc_best_child(self, debug=False):
        # Make sure there is at least one child node
        if len(self.get_children()) == 0:
            raise IllegalNumberOfChildrenException("Error: Not enough children!")

        # Fill a list with all the scores of the children of the current node
        child_score_list = []
        best_child = None
        best_score = None
        if self.get_state().get_current_turn() == self.get_state().get_starting_player():
            best_score = -9999
        elif self.get_state().get_current_turn() == self.get_state().get_second_player():
            best_score = 9999

        for child in self.get_children():
            if child.get_score() == [0, 0]:
                exploitation_bonus = 0
                exploration_bonus = 0
            else:
                exploitation_bonus = child.get_score()[1] / child.get_score()[0]
                exploration_bonus = self.calc_u_s_a(child)

            if self.get_state().get_current_turn() == self.get_state().get_starting_player():
                score = exploitation_bonus + exploration_bonus
                child_score_list.append(score)
                if score > best_score:
                    best_score = score
                    best_child = child
            elif self.get_state().get_current_turn() == self.get_state().get_second_player():
                score = exploitation_bonus - exploration_bonus
                child_score_list.append(score)
                if score < best_score:
                    best_score = score
                    best_child = child

        if debug:
            print(child_score_list)

        return best_child


    # Alternative to calc_best_child
    def get_child_with_highest_visit_count(self):
        if len(self.get_children()) == 0:
            raise IllegalNumberOfChildrenException("Error: Not enough children!")

        best_child = self.get_children()[0]

        for child in self.get_children():
            if child.get_score()[0] > best_child.get_score()[0]:
                best_child = child

        return best_child


    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_score()[0]
        N_s = self.get_score()[0]

        return self.c * math.sqrt(math.log(N_s, 10) / (1 + N_s_a))


    #############################
    # ANET CONVERSION FUNCTIONS #
    #############################

    # Choose child node based on anet's predictions
    def get_anet_position_prediction(self, anet):
        # Get the anet_compatible board format
        board_p1_p2 = self.merge_boards_to_anet()

        board_p1_p2 = board_p1_p2.reshape(1, self.get_state().get_board().get_board_size(),
                            self.get_state().get_board().get_board_size(), 2)

        action_probs = self.tf_test(anet, board_p1_p2)

        # Set value of occupied moves to 0 (zero probability to pick these)
        action_probs = action_probs * self.get_valid_moves().flatten()

        action_probs = action_probs / np.sum(action_probs)

        return np.array(action_probs)


    # 'Merge' the boards to a single array to make them compatible to be read by the anet
    def merge_boards_to_anet(self):
        board_p1 = self.get_state().get_board().get_board_np_p1()
        board_p2 = self.get_state().get_board().get_board_np_p2()
        board_size = self.get_state().get_board().get_board_size()
        board_p1_p2 = np.zeros(shape=(board_size, board_size, 2), dtype=int)
        for y in range(board_size):
            for x in range(board_size):
                if self.get_state().get_current_turn() == self.get_state().get_starting_player():
                    board_p1_p2[y, x] = [board_p1[y, x], 0]
                elif self.get_state().get_current_turn() == self.get_state().get_second_player():
                    board_p1_p2[y, x] = [board_p2[y, x], 1]

        return board_p1_p2


    def tf_test(self, anet, input):

        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_content=anet)
        interpreter.allocate_tensors()

        # get input and output tensors
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Preprocess the image to required size and cast
        input_shape = input_details[0]['shape']
        input_tensor = input
        input_tensor = np.array(input, dtype=np.float32)

        # set the tensor to point to the input data to be inferred
        input_index = interpreter.get_input_details()[0]["index"]
        interpreter.set_tensor(input_index, input_tensor)

        # Run the inference
        interpreter.invoke()
        output_index = interpreter.get_output_details()[0]["index"]
        output_tensor = interpreter.get_tensor(output_index)
        output_array = np.squeeze(output_tensor)

        return output_array