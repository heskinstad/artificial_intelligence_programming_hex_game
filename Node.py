import copy
import random

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
        # TODO: Add to score when backtracking after each simulation

    def get_state(self):
        return self.state

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

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

    def create_child_nodes(self, depth):
        if depth > 0:

            board = self.get_state().get_board()

            for x in range(board.get_board_size()):
                for y in range(board.get_board_size()):
                    if board.get_hex_by_x_y(x, y).get_occupation_status() == None:

                        board_deepcopy = copy.deepcopy(board)

                        board_deepcopy.place(self.get_state().get_current_turn(), x, y)

                        #board_deepcopy.get_hex_by_column_row(i, j).set_occupation_status(self.get_state().get_current_turn())

                        child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn()), self)

                        self.add_child(child)

                        child.create_child_nodes(depth - 1)

    def check_if_child_nodes_finished(self):
        for child in self.get_children():
            if child.get_score() == [0, 0]:
                return 0
        return 1

    def simulate_from_node(self, player, opposing_player, max_depth):
        if max_depth <= 0:
            return
        max_depth -= 1

        if len(self.get_children()) == 0:
            self.create_child_nodes(1)

        for child in self.get_children():
            # If player won this simulation
            if child.get_state().get_board().check_if_player_won(player) == player:
                #print('REDVICTORY')
                child.player_victory()
                child.make_leaf()

            # If player lost this simulation
            elif child.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
                #print('BLUEVICTORY')
                child.opposing_player_victory()
                child.make_leaf()

            if not child.is_leaf():
                child.simulate_from_node(player, opposing_player, max_depth)

            self.add_score_from_child(child)


        # Delete objects without optimal score
        if len(self.get_children()) > 0:
            best_child = self.get_children()[0]

            # Iterate through the children and set best_child to be the best (highest score for red, lowest score for blue)
            if self.get_state().get_current_turn() == player:
                for child in self.get_children():
                    if ((child.get_score()[1]+1) / (child.get_score()[0]+1)) > ((best_child.get_score()[1]+1) / (best_child.get_score()[0]+1)):
                        best_child = child
            elif self.get_state().get_current_turn() == opposing_player:
                for child in self.get_children():
                    if ((child.get_score()[1]+1) / (child.get_score()[0]+1)) < ((best_child.get_score()[1]+1) / (best_child.get_score()[0]+1)):
                        best_child = child

            i = 0
            while len(self.get_children()) > 1:
                if not self.get_children()[i].get_score() == best_child:
                    del self.get_children()[i]
                else:
                    i += 1

    def mcts_default_policy_to_leaf_node(self, player, opposing_player):
        print()
        self.get_state().get_board().print_board()
        # If player won this simulation
        if self.get_state().get_board().check_if_player_won(player) == player:
            print('REDVICTORY')
            self.player_victory()
            self.make_leaf()
        # If player lost this simulation
        elif self.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
            print('BLUEVICTORY')
            self.opposing_player_victory()
            self.make_leaf()

        if not self.is_leaf():

            if len(self.get_children()) == 0:
                self.create_child_nodes(1)

            # Select a random child node and delete all other child nodes
            child_node = random.choice(self.get_children())

            i = 0
            while len(self.get_children()) > 1:
                if not self.get_children()[i] == child_node:
                    del self.get_children()[i]
                else:
                    i += 1

            child_node.mcts_default_policy_to_leaf_node(player, opposing_player)

            self.add_score_from_child(child_node)

    # Traverse down the tree to the best known leaf node
    def move_to_best_node(self):
        if len(self.get_children()) > 0:
            print()
            self.get_children()[0].get_state().get_board().print_board()
            return self.get_children()[0].move_to_best_node()
        else:
            return self