from Board import Board

class State:
    def __init__(self, board, current_turn, next_turn):
        self.board = board
        self.current_turn = current_turn
        self.next_turn = next_turn

    def get_board(self):
        return self.board

    def get_current_turn(self):
        return self.current_turn

    def get_next_turn(self):
        return self.next_turn

    def create_next_state(self):
        return Board(self.board.get_board_size(), False)