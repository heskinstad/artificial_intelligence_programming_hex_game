import math
import random

from Board import Board
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
    def mcts_tree_policy(self):
        pass


    def mcts_default_policy(self):
        pass


    def node_check_win(self, player, opposing_player):
        # If player won this simulation
        if self.get_state().get_board().check_if_player_won(player) == player:
            self.player_victory()
            self.make_endstate()
            return [1, 1]
        # If player lost this simulation
        elif self.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
            self.opposing_player_victory()
            self.make_endstate()
            return [1, 0]


    # Calculate exploration bonus. Parameter child can be viewed as the action
    def calc_u_s_a(self, child):
        N_s_a = child.get_visits() + 1
        N_s = self.get_visits()

        return self.c * math.sqrt(math.log(N_s) / (1 + N_s_a))


    def calc_best_child(self, player, opposing_player):
        pass


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