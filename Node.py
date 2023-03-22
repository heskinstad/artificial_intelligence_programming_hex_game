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
        self.total_score = None

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


    def check_if_child_nodes_finished(self):
        for child in self.get_children():
            if child.get_score() == [0, 0]:
                return 0
        return 1


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
        self.add_visit()
        self.node_check_win(player, opposing_player)

        if not self.is_leaf():
            if len(self.get_children()) > 0:
                best_child = self.calc_best_child(player, opposing_player)

                if best_child.get_visits() < 6 * len(self.get_children()):
                    best_child.mcts_tree_policy(player, opposing_player)
                    return

            # Try to create a new child node
            child = self.create_random_child_node()

            # child is None if there are no available child node slots
            if child == None:
                print(len(self.get_children()))
                child = random.choice(self.get_children())
                child.mcts_tree_policy(player, opposing_player)
                return

            child.mcts_default_policy(player, opposing_player)

        else:
            self.win_end_game(player, opposing_player)


    def mcts_default_policy(self, player, opposing_player):
        self.add_visit()
        self.node_check_win(player, opposing_player)

        if not self.is_leaf():
            child_node = self.create_random_child_node()

            # If there are no possible child nodes left (no free positions on the board)
            if child_node == None:
                return

            child_node.mcts_default_policy(player, opposing_player)

        # Propagate the score and visit up every node in the current path to the top node
        else:
            self.win_end_game(player, opposing_player, True)


    def win_end_game(self, player, opposing_player, remove_children=False):
        child = self
        current = self.get_parent()

        while current.get_parent() != None:
            current.add_score_from_child(child)
            current.add_visit()

            child = current
            current = current.get_parent()

        current.add_score_from_child(child)
        current.add_visit()

        if remove_children:
            self.remove_all_children()

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

    #TODO: make it select the best child based on the total score instead of win/loss ratio?
    def remove_every_but_best_child(self, player, opposing_player):
        # Delete objects without optimal score
        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            if self.get_state().get_current_turn() == player:
                for child in self.get_children():
                    '''if child.node_check_win(player, opposing_player):
                        best_child = child
                        child.score[1] += 100  # Add a very large value for red to choose this
                        print(player.get_color() + " is about to win")
                        break'''

                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) > ((best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child

            elif self.get_state().get_current_turn() == opposing_player:
                for child in self.get_children():
                    '''if child.node_check_win(player, opposing_player):
                        best_child = child
                        child.score[1] -= 100  # Add a very large (negative) value for blue to choose this
                        print(opposing_player.get_color() + " is about to win")
                        break'''

                    if ((child.get_score()[1] + 1) / (child.get_score()[0] + 1)) < ((best_child.get_score()[1] + 1) / (best_child.get_score()[0] + 1)):
                        best_child = child

            i = 0
            while len(self.get_children()) > 1:
                if not self.get_children()[i] == best_child:
                    del self.get_children()[i]
                else:
                    i += 1

    def remove_every_but_best_child2(self, player, opposing_player):
        # Delete objects without optimal score
        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            if self.get_state().get_current_turn() == player:
                for child in self.get_children():
                    if child.get_total_score() > best_child.get_total_score():
                        best_child = child

            elif self.get_state().get_current_turn() == opposing_player:
                for child in self.get_children():
                    if child.get_total_score() < best_child.get_total_score():
                        best_child = child

            i = 0
            while len(self.get_children()) > 1:
                if not self.get_children()[i] == best_child:
                    del self.get_children()[i]
                else:
                    i += 1


    # Traverse down the tree to the best known leaf node
    def expand_through_best_node(self, player, opposing_player):
        if len(self.get_children()) > 0:
            all_without_total_score = True
            for child in self.get_children():
                if child.get_total_score != None:
                    all_without_total_score = False
                    break

            if all_without_total_score:
                return self

            best_child = self.calc_best_child(player, opposing_player)

            best_child.mcts_default_policy(player, opposing_player)

        else:
            return self

    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_visits() + 1
        N_s = self.get_visits()

        return self.c * math.sqrt(math.log(N_s) / (1 + N_s_a))


    def calc_best_child(self, player, opposing_player):
        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            for child in self.get_children():
                if child.get_score()[0] == 0:
                    exploitation_bonus = 0
                else:
                    exploitation_bonus = child.get_score()[1] / child.get_score()[0]

                exploration_bonus = self.calc_u_s_a(child)

                if self.get_state().get_current_turn() == player:
                    # Player want the highest score
                    child.set_total_score(exploitation_bonus + exploration_bonus)
                    if child.get_total_score() > best_child.get_total_score():
                        best_child = child

                elif self.get_state().get_current_turn() == opposing_player:
                    # Opposing player want the lowest score
                    child.set_total_score(exploitation_bonus - exploration_bonus)
                    if child.get_total_score() < best_child.get_total_score():
                        best_child = child

            return best_child

        else:
            raise IllegalNumberOfChildrenException("node needs to have at least one child")


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