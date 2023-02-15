import copy

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

    def get_leaf(self):
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

    def check_if_child_nodes_finished(self):
        for child in self.get_children():
            if child.get_score() == [0, 0]:
                return 0
        return 1

    def simulate_from_node(self, player, opposing_player):
        if len(self.get_children()) == 0:
            self.create_child_nodes_for_player(player, opposing_player, 1)

        for child in self.get_children():
            # If player won this simulation
            if child.get_state().get_board().check_if_player_won(player) == player:
                child.player_victory()
                child.make_leaf()
                self.player_victory()
                return

            # If player lost this simulation
            elif child.get_state().get_board().check_if_player_won(opposing_player) == opposing_player:
                child.opposing_player_victory()
                child.make_leaf()
                self.opposing_player_victory()
                return

            child.simulate_all()