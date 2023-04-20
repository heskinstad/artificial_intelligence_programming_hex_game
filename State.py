from Board import Board

# The State class keeps information about the current board and which player's turn it is
class State:
    def __init__(self, board, current_turn, next_turn, start_turn, second_turn):
        self.board = board
        self.current_turn = current_turn
        self.next_turn = next_turn
        self.starting_player = start_turn
        self.second_player = second_turn

    def get_board(self):
        return self.board

    def get_current_turn(self):
        return self.current_turn

    def get_next_turn(self):
        return self.next_turn

    def set_current_next_turn(self, current_turn, next_turn):
        self.current_turn = current_turn
        self.next_turn = next_turn

    def set_starting_player(self, player):
        self.starting_player = player

    def get_starting_player(self):
        return self.starting_player

    def set_second_player(self, player):
        self.second_player = player

    def get_second_player(self):
        return self.second_player

    def create_next_state(self):
        return Board(self.board.get_board_size(), False)