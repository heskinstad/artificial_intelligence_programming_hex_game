class State:
    def __init__(self, board, currentTurn):
        self.board = board
        self.currentTurn = currentTurn

    def GetBoard(self):
        return self.board

    def GetCurrentTurn(self):
        return self.currentTurn