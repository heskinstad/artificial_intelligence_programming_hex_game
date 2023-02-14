import copy

from State import State


class Node:
    def __init__(self, state, parent=None, score=None):
        if score is None:
            score = [0, 0]
        self.state = state
        self.parent = parent
        self.children = []
        self.score = score # Holds the accumulated [number_of_wins, number_of_nodes] score
        # TODO: Add to score when backtracking after each simulation

    def get_state(self):
        return self.state

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

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

    def create_child_nodes_for_player(self, player, other_player, depth):
        if depth > 0:

            board = self.get_state().get_board()

            for i in range(board.get_board_size()):
                for j in range(board.get_board_size()):
                    if board.get_hex_by_column_row(i, j).get_occupation_status() == None:

                        board_deepcopy = copy.deepcopy(board)

                        board_deepcopy.get_hex_by_column_row(i, j).set_occupation_status(player)

                        child = Node(State(board_deepcopy, self.get_state().get_next_turn(), self.get_state().get_current_turn()), self)

                        self.add_child(child)

                        child.create_child_nodes_for_player(other_player, player, depth-1)