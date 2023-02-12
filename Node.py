from State import State


class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def replace_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)

    def remove_child_at_index(self, index):
        self.children.remove(index)

    def create_child_nodes_for_player(self, player):
        board = self.get_state().get_board()

        for i in range(board.get_board_size()):
            for j in range(board.get_board_size()):
                if board.get_hex_by_column_row(i, j).get_occupation_status() == None:
                    print(board.get_hex_by_column_row(i, j).get_occupation_status())
                    board.get_hex_by_column_row(i, j).set_occupation_status(player)
                    print(board.get_hex_by_column_row(i, j).get_occupation_status())
                    self.add_child(Node(State(board, self.get_state().get_next_turn(), self.get_state().get_current_turn())))
                    board.get_hex_by_column_row(i, j).set_occupation_status(None)

    def print_all_child_nodes(self):
        for child in self.get_children():
            child.get_state().get_board().print_board()