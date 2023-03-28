import math
import random

from Board import Board
from Exceptions.IllegalNumberOfChildrenException import IllegalNumberOfChildrenException
from State import State

class Node:
    def __init__(self, state, parent=None, score=None, endstate=False):
        if score is None:
            score = [0, 0]
        self.state = state
        self.parent = parent
        self.children = []
        self.score = score # Holds the accumulated [number_of_wins, number_of_nodes] score
        self.endstate = endstate
        self.c = None
        self.visits = 0
        self.total_score = None
        self.leaf = False
        self.top_node = False

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

    def add_visit(self):
        self.visits += 1

    def get_visits(self):
        return self.visits

    def player_victory(self):
        self.score[0] += 1
        self.score[1] += 1

    def opposing_player_victory(self):
        self.score[0] += 1

    def add_score_from_child(self, child):
        self.score[0] += child.score[0]
        self.score[1] += child.score[1]

    def set_total_score(self, total_score):
        self.total_score = total_score

    def get_total_score(self):
        return self.total_score

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

    def remove_child_at_index(self, index):
        self.children.remove(index)

    def remove_all_children(self):
        self.children = []

    def set_as_top_node(self):
        self.top_node = True

    def is_top_node(self):
        return self.top_node

    def create_child_nodes(self, depth):
        if depth > 0:

            board = self.get_state().get_board()

            for x in range(board.get_board_size()):
                for y in range(board.get_board_size()):
                    if board.get_hex_by_x_y(x, y) == None:

                        board_deepcopy = Board(board.get_board_size(), False)
                        board_deepcopy.board_positions = [x[:] for x in board.get_board()]

                        board_deepcopy.place(self.get_state().get_current_turn(), x, y)

                        child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn()), self)
                        child.set_c(self.get_c())

                        self.add_child(child)
                        child.set_parent(self)

                        child.create_child_nodes(depth - 1)


    # Create a single, randomized child node
    def create_random_child_node(self):
        board = self.get_state().get_board()

        # Create a 'board' with coordinates
        positions = []
        for y in range(board.get_board_size()):
            for x in range(board.get_board_size()):
                positions.append([y, x])

        while len(positions) > 1:

            # Select x and y randomly from the available positions
            index = int(random.uniform(0, len(positions)))
            x = positions[index][1]
            y = positions[index][0]

            # Check if it already exists in any of the other children nodes
            in_current_child = False
            if len(self.get_children()) > 0:
                for child in self.get_children():
                    if child.get_state().get_board().get_hex_by_x_y(x, y) != None:
                        in_current_child = True

            if board.get_hex_by_x_y(x, y) == None and not in_current_child:

                board_deepcopy = Board(board.get_board_size(), False)
                board_deepcopy.board_positions = [x[:] for x in board.get_board()]

                board_deepcopy.place(self.get_state().get_current_turn(), x, y)

                child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn()), self)
                child.c = self.get_c()

                self.add_child(child)

                return child

            # If the space is occupied, delete the position from the array and try again
            else:
                del positions[index]

        # Return None if there are no free spaces left
        return None


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
    def mcts_tree_policy(self, player, opposing_player):
        # If self is a leaf it will have no children and needs to use the default policy
        if self.is_leaf():
            self.mcts_default_policy(player, opposing_player)
            self.remove_leaf_status()
            return

        elif self.is_endstate():
            return

        best_child = self.calc_best_child(player, opposing_player)

        best_child.mcts_tree_policy(player, opposing_player)


    # A run of the default policy is one rollout
    def mcts_default_policy(self, player, opposing_player):
        score = self.node_check_win(player, opposing_player)

        # If anyone won in this node
        if score != 0:
            self.make_endstate()
            self.propagate_score(score)
            print(score)
            return

        # Choose a random child node and move to this recursively
        random_child_node = self.create_random_child_node()
        random_child_node.mcts_default_policy(player, opposing_player)

        # If top node in the newly generated default policy tree
        # Remove own children and set itself as a leaf
        if self.get_parent() != None:
            if self.get_parent().is_leaf():
                self.remove_all_children()
                self.set_leaf_status()
        else:
            return


    # Propagates the score given as a parameter to the node self and every parent up throughout the tree
    def propagate_score(self, score):
        current_node = self

        # Go up to every parent and add score until there are no parents
        while current_node.get_parent() != None:
            current_node.set_score([current_node.get_score()[0] + score[0], current_node.get_score()[1] + score[1]])
            current_node = current_node.get_parent()


    def node_check_win(self, player, opposing_player):
        # If player won this simulation
        if self.get_state().get_board().check_if_player_won(player) == player:
            self.make_endstate()
            return [1, 1]
        # If player lost this simulation
        elif self.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
            self.make_endstate()
            return [1, -1]
        else:
            return 0


    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_score()[0]
        N_s = self.get_score()[0]

        return self.c * math.sqrt(math.log(N_s) / (1 + N_s_a))


    # Return the child with the best score relative to the current player
    def calc_best_child(self, player, opposing_player):
        # Make sure there is at least one child node
        if len(self.get_children()) == 0:
            raise IllegalNumberOfChildrenException("Error: Not enough children!")

        # Fill a list with all the scores of the children of the current node
        scores_list = []
        for child in self.get_children():
            if self.get_score() == [0, 0]:
                exploitation_bonus = 0
                exploration_bonus = 0
            else:
                exploitation_bonus = self.get_score()[1] / self.get_score()[0]
                exploration_bonus = self.calc_u_s_a(child)

            if self.get_state().get_current_turn() == player:
                scores_list.append(exploitation_bonus + exploration_bonus)
            elif self.get_state().get_current_turn() == opposing_player:
                scores_list.append(exploitation_bonus - exploration_bonus)

        # Iterate through this list and get the index of the best child
        # Best child is the one with the highest score for player
        # and the one with the lowest score for opposing_player
        best_score_index = 0
        for i in range(len(scores_list)):
            if self.get_state().get_current_turn() == player:
                if scores_list[i] > scores_list[best_score_index]:
                    best_score_index = i
            elif self.get_state().get_current_turn() == opposing_player:
                if scores_list[i] < scores_list[best_score_index]:
                    best_score_index = i

        return self.get_children()[best_score_index]



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