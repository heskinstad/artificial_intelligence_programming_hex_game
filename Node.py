import math
import random
import time

from Board import Board
from Exceptions.IllegalNumberOfChildrenException import IllegalNumberOfChildrenException
from State import State

class Node:
    def __init__(self, state, parent=None, score=None, leaf=False):
        if score is None:
            score = [0, 0]
        self.state = state
        self.parent = parent
        self.children = []
        self.score = score # Holds the accumulated [number_of_wins, number_of_nodes] score
        self.leaf = leaf
        self.c = None
        self.visits = 0

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

    def is_leaf(self):
        return self.leaf

    def make_leaf(self):
        self.leaf = True

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
        while True:
            x = int(random.uniform(0, board.get_board_size()))
            y = int(random.uniform(0, board.get_board_size()))
            if board.get_hex_by_x_y(x, y) == None:

                board_deepcopy = Board(board.get_board_size(), False)
                board_deepcopy.board_positions = [x[:] for x in board.get_board()]

                board_deepcopy.place(self.get_state().get_current_turn(), x, y)

                child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn()), self)

                self.add_child(child)

                return child


    def check_if_child_nodes_finished(self):
        for child in self.get_children():
            if child.get_score() == [0, 0]:
                return 0
        return 1

    ''' old stuff - TO BE REMOVED
    def simulate_from_node(self, player, opposing_player, max_depth):
        if max_depth <= 0:
            return
        max_depth -= 1

        if len(self.get_children()) == 0:
            self.create_child_nodes(1)

        for child in self.get_children():
            child.node_check_win(player, opposing_player)

            if not child.is_leaf():
                child.simulate_from_node(player, opposing_player, max_depth)

            self.add_score_from_child(child)

        self.remove_every_but_best_child(player, opposing_player)
    '''

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
    def mcts_tree_policy(self, player, opposing_player, max_depth, max_time):
        if max_depth <= 0:
            self.mcts_default_policy(player, opposing_player)
            return
        max_depth -= 1

        if len(self.get_children()) == 0:
            self.create_child_nodes(1)

        time_start = time.time()

        for child in self.get_children():
            if time.time() > time_start + max_time:
                self.add_score_from_child(child)
                self.remove_every_but_best_child(player, opposing_player)
                return

            # Makes child leaf if end state (win or loss)
            child.node_check_win(player, opposing_player)

            if not child.is_leaf():
                child.mcts_tree_policy(player, opposing_player, max_depth, max_time)

            self.add_score_from_child(child)
            self.add_visit()
            child.add_visit()

        self.remove_every_but_best_child(player, opposing_player)
        print(self.calc_u_s_a(self.get_children()[0]))

    def mcts_tree_policy(self, player, opposing_player, max_depth, max_time):
        if max_depth <= 0:
            self.mcts_default_policy(player, opposing_player)
            return
        max_depth -= 1

        if len(self.get_children()) == 0:
            self.create_child_nodes(1)

        time_start = time.time()

        for child in self.get_children():
            if time.time() > time_start + max_time:
                self.add_score_from_child(child)
                self.remove_every_but_best_child(player, opposing_player)
                return

            # Makes child leaf if end state (win or loss)
            child.node_check_win(player, opposing_player)

            if not child.is_leaf():
                child.mcts_tree_policy(player, opposing_player, max_depth, max_time)

            self.add_score_from_child(child)
            self.add_visit()
            child.add_visit()

        self.remove_every_but_best_child(player, opposing_player)
        print(self.calc_u_s_a(self.get_children()[0]))

    def mcts_default_policy(self, player, opposing_player):
        self.node_check_win(player, opposing_player)

        if not self.is_leaf():
            child_node = self.create_random_child_node()

            child_node.mcts_default_policy(player, opposing_player)

            self.add_score_from_child(child_node)

    def node_check_win(self, player, opposing_player):
        # If player won this simulation
        if self.get_state().get_board().check_if_player_won(player) == player:
            self.player_victory()
            self.make_leaf()
            return 1
        # If player lost this simulation
        elif self.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
            self.opposing_player_victory()
            self.make_leaf()
            return 1

    def remove_every_but_best_child(self, player, opposing_player):
        # Delete objects without optimal score
        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            if self.get_state().get_current_turn() == player:
                for child in self.get_children():
                    if child.node_check_win(player, opposing_player):
                        best_child = child
                        child.score[1] += 100  # Add a very large value for red to choose this
                        print(player.get_color() + " is about to win")
                        break

                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) > ((best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child

            elif self.get_state().get_current_turn() == opposing_player:
                for child in self.get_children():
                    if child.node_check_win(player, opposing_player):
                        best_child = child
                        child.score[1] -= 100  # Add a very large (negative) value for blue to choose this
                        print(opposing_player.get_color() + " is about to win")
                        break

                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) < ((best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child

            i = 0
            while len(self.get_children()) > 1:
                if not self.get_children()[i] == best_child:
                    del self.get_children()[i]
                else:
                    i += 1

    # Traverse down the tree to the best known leaf node
    def move_to_best_node(self, depth):

        if self.is_leaf():
            return self

        if len(self.get_children()) > 0 and depth > 0:

            if len(self.get_children()) > 1:
                raise IllegalNumberOfChildrenException("There can only be one child per node")

            print()
            print(self.get_score())
            self.get_children()[0].get_state().get_board().print_board()

            return self.get_children()[0].move_to_best_node(depth - 1)
        else:
            self.remove_all_children()
            return self

    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_visits() + 1
        N_s = self.get_visits()

        return self.c * math.sqrt(math.log(N_s) / (1 + N_s_a))

    def calc_best_child(self, player, opposing_player):
        exploration_bonus = self.calc_u_s_a()

        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            if self.get_state().get_current_turn() == player:
                for child in self.get_children():

                    # Player want the highest score
                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) > (
                            (best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child

            elif self.get_state().get_current_turn() == opposing_player:
                for child in self.get_children():

                    # Opposing player want the lowest score
                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) < (
                            (best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child