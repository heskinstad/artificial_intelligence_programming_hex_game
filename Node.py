import copy
import math
import random
import time

import numpy as np

from Board import Board
from Exceptions.IllegalNumberOfChildrenException import IllegalNumberOfChildrenException
from State import State

class Node:
    def __init__(self, state, max_children, parent=None, score=None, endstate=False):
        if score is None:
            score = [0, 0]
        self.state = state
        self.parent = parent
        self.children = []
        self.score = score # Holds the accumulated [number_of_visits, score]
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

    def create_child_nodes(self, depth):
        if depth > 0:

            board = self.get_state().get_board()

            for x in range(board.get_board_size()):
                for y in range(board.get_board_size()):
                    if board.get_hex_by_x_y(x, y) == 0:

                        board_deepcopy = Board(board.get_board_size(), False)
                        board_deepcopy.board_positions = [x[:] for x in board.get_board()]

                        board_deepcopy.place(self.get_state().get_current_turn(), x, y)

                        child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()), self.get_max_children() - 1, self)
                        child.set_c(self.get_c())

                        self.add_child(child)
                        child.set_parent(self)

                        child.create_child_nodes(depth - 1)


    # Create a single, randomized child node
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

    '''
    Tree policy:
    Choose the branch with the highest combination of exploitation + exploration
    Q(s, a) + u(s, a)
    where
    Q(s, a) is the value of the final expected result of doing action a from node s (updated after each rollout)
    - can be considered the score of a child node?
    and
    u(s, a) is 
    '''
    def mcts_tree_policy(self, node_expansion=1):
        # If self is a leaf it will have no children and needs to use the default policy
        if self.is_endstate():
            return
        # Expand with default policy if:
        # Node is leaf or
        # The current number of nodes on this level is less than half of the maximum number of nodes on this level
        elif self.is_leaf() or len(self.get_children()) < (self.get_max_children() - 1) / node_expansion:
            self.set_leaf_status()
            self.mcts_default_policy()
            self.remove_leaf_status()
        else:
            best_child = self.calc_best_child()
            best_child.mcts_tree_policy(node_expansion)


    # A run of the default policy is one rollout
    def mcts_default_policy(self):
        score = self.node_check_win()

        # If anyone won in this node
        if self.is_endstate():
            self.propagate_score(score)
            return

        # Choose a random child node and move to this recursively
        random_child_node = self.create_random_child_node()
        if random_child_node == None:  # Is none if there is only a single child left and it has already been created
            self.get_children()[0].mcts_default_policy()
        else:
            random_child_node.mcts_default_policy()

        # If top node in the newly generated default policy tree
        # Remove own children and set itself as a leaf
        if self.get_parent() != None:
            if self.get_parent().is_leaf():
                self.remove_all_children()
                self.set_leaf_status()
        else:
            return


    def anet_policy(self, anet):
        # Create the array of the current game board in one dimension and append the id of the current player
        p1_board = self.get_state().get_board().get_board_np_p1()
        p2_board = self.get_state().get_board().get_board_np_p2()
        board_size = self.get_state().get_board().get_board_size()
        ohe = np.zeros(shape=(board_size, board_size, 2))
        for i in range(board_size):
            for j in range(board_size):
                if self.get_state().get_current_turn() == self.get_state().get_starting_player():
                    ohe[i, j] = [p1_board[i, j], p2_board[i, j]]
                elif self.get_state().get_current_turn() == self.get_state().get_second_player():
                    ohe[i, j] = [p2_board.T[i, j], p1_board.T[i, j]]

        array = ohe

        # Create the array of the current game board
        # if self.get_state().get_current_turn() == self.get_state().get_starting_player():
        #    array = self.get_state().get_board().get_board_np_p1()
        # elif self.get_state().get_current_turn() == self.get_state().get_second_player():
        #    array = self.get_state().get_board().get_board_np_p2()

        array = array.reshape(1, self.get_state().get_board().get_board_size(), self.get_state().get_board().get_board_size(), 2)

        action_probs = anet(array)[0]

        valid_moves = self.get_valid_moves(action_probs).flatten()

        action_probs = action_probs * valid_moves
        action_probs = action_probs / np.sum(action_probs)

        action_probs = np.array(action_probs)

        action_probs = action_probs / np.sum(action_probs)
        try:
            action_idx = np.random.choice(len(action_probs), p=action_probs)
            #action_idx = np.argmax(action_probs)
        except:  # If action_probs contains nan (meaning the network only predicted impossible moves)
            print("Network predicted impossible values. Choosing random node.")
            valid_moves = valid_moves / np.sum(valid_moves)
            action_idx = np.random.choice(len(valid_moves), p=valid_moves)



        #tete = 2.0
        #for i in range(len(action_probs)):
        #    if action_probs[i] < tete and action_probs[i] > 0.0:
        #         tete = action_probs[i]
        #         action_idx = i

        return action_idx


    def get_valid_moves(self, predictions):
        valid_moves = copy.deepcopy(self.get_state().get_board().get_board_np_p1())
        for y in range(len(valid_moves)):
            for x in range(len(valid_moves[y])):
                if valid_moves[y][x] == 0:
                    valid_moves[y][x] = 1
                else:
                    valid_moves[y][x] = 0

        return valid_moves


    # Propagates the score given as a parameter to the node self and every parent up throughout the tree
    def propagate_score(self, score):
        current_node = self

        # Go up to every parent and add score until there are no parents
        while current_node.get_parent() != None:
            current_node.set_score([current_node.get_score()[0] + score[0], current_node.get_score()[1] + score[1]])
            current_node = current_node.get_parent()

        current_node.set_score([current_node.get_score()[0] + score[0], current_node.get_score()[1] + score[1]])


    def node_check_win(self, return_player=False):
        # If player won this simulation
        #if self.get_state().get_board().check_if_player_won(player) == player:
        if self.get_state().get_board().check_if_player_won(self.get_state().get_current_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()) == self.get_state().get_starting_player()\
                or self.get_state().get_board().check_if_player_won(self.get_state().get_next_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()) == self.get_state().get_starting_player():
            self.make_endstate()
            if return_player:
                return self.get_state().get_starting_player()
            return [1, 1]
        # If player lost this simulation
        #elif self.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
        elif self.get_state().get_board().check_if_player_won(self.get_state().get_current_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()) == self.get_state().get_second_player()\
                or self.get_state().get_board().check_if_player_won(self.get_state().get_next_turn(), self.get_state().get_starting_player(), self.get_state().get_second_player()) == self.get_state().get_second_player():
            self.make_endstate()
            if return_player:
                return self.get_state().get_second_player()
            return [1, -1]
        else:
            return 0


    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_score()[0]
        N_s = self.get_score()[0]

        return self.c * math.sqrt(math.log(N_s, 10) / (1 + N_s_a))


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

    def get_child_with_highest_visit_count(self):
        if len(self.get_children()) == 0:
            raise IllegalNumberOfChildrenException("Error: Not enough children!")

        best_child = self.get_children()[0]

        for child in self.get_children():
            #if child.is_endstate():
            #    best_child = child
            #    break
            if child.get_score()[0] > best_child.get_score()[0]:
                best_child = child

        return best_child


    # Print the path (index number of every node down to the current node)
    def get_path(self):
        path = ""
        current = self

        while current.get_parent() != None:
            index = 0
            for i in range(len(current.get_parent().get_children())):
                if current.get_parent().get_children()[i] == current:
                    index = i
                    break

            path = str(index) + " " + path

            current = current.get_parent()

        return path

    def mcts_tree_policy2(self, node_expansion=1, anet=None):
        # If self is a leaf it will have no children and needs to use the default policy
        if self.is_endstate():
            return
        # Expand with default policy if:
        # Node is leaf or
        # The current number of nodes on this level is less than half of the maximum number of nodes on this level
        elif self.is_leaf() or len(self.get_children()) < (self.get_max_children() - 1) / node_expansion:
            self.set_leaf_status()
            self.mcts_default_policy2(anet)
            self.remove_leaf_status()
        else:
            best_child = self.calc_best_child()
            best_child.mcts_tree_policy2(node_expansion, anet)


    def mcts_default_policy2(self, anet=None):
        score = self.node_check_win()

        # If anyone won in this node
        if self.is_endstate():
            self.propagate_score(score)
            return

        p1_board = self.get_state().get_board().get_board_np_p1()
        p2_board = self.get_state().get_board().get_board_np_p2()
        board_size = self.get_state().get_board().get_board_size()
        ohe = np.zeros(shape=(board_size, board_size, 2))
        for i in range(board_size):
            for j in range(board_size):
                if self.get_state().get_current_turn() == self.get_state().get_starting_player():
                    ohe[i, j] = [p1_board[i, j], p2_board[i, j]]
                elif self.get_state().get_current_turn() == self.get_state().get_second_player():
                    ohe[i, j] = [p2_board.T[i, j], p1_board.T[i, j]]

        array = ohe

        # Create the array of the current game board
        #if self.get_state().get_current_turn() == self.get_state().get_starting_player():
        #    array = self.get_state().get_board().get_board_np_p1()
        #elif self.get_state().get_current_turn() == self.get_state().get_second_player():
        #    array = self.get_state().get_board().get_board_np_p2()

        array = array.reshape(1, self.get_state().get_board().get_board_size(), self.get_state().get_board().get_board_size(), 2)

        action_probs = anet(array)[0]

        action_probs = action_probs * self.get_valid_moves(action_probs).flatten()

        action_probs = np.array(action_probs)

        random_child_node = None
        if self.get_max_children() == len(self.get_children()):
            random_child_node = random.choice(self.get_children())
            return

        while random_child_node == None:
            if np.isnan(action_probs[5]) or np.isnan(action_probs[2]):
                return
            action_probs = action_probs / np.sum(action_probs)
            #action_idx = np.random.choice(len(action_probs), p=action_probs)
            action_idx = np.argmax(action_probs)

            position = [None, None]
            position[0] = math.floor(action_idx / self.get_state().get_board().get_board_size())
            position[1] = action_idx % self.get_state().get_board().get_board_size()

            random_child_node = self.create_random_child_node(position)

            action_probs[action_idx] = 0.0

        random_child_node.mcts_default_policy2(anet)

        # Choose a random child node and move to this recursively
        #random_child_node = self.create_random_child_node()
        #if random_child_node == None:  # Is none if there is only a single child left and it has already been created
        #    self.get_children()[0].mcts_default_policy(player, opposing_player)
        #else:
        #    random_child_node.mcts_default_policy(player, opposing_player)

