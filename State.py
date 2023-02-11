class State:
    def __init__(self, board, current_turn):
        self.board = board
        self.current_turn = current_turn

    def get_board(self):
        return self.board

    def get_current_turn(self):
        return self.current_turn