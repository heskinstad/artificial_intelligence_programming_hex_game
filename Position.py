from Board import Board

class Position(Board):
    def __init__(self, column, row, hex, occupiedBy, board_size):
        super().__init__(board_size)
        self.row = row
        self.column = column
        self.hex = hex
        self.occupiedBy = occupiedBy
        self.board_size = board_size

    def GetRow(self):
        return self.row

    def GetColumn(self):
        return self.column

    def GetCoordinates(self):
        return str([self.column, self.row])

    def GetHex(self):
        return self.hex

    def SetOccupationStatus(self, occupiedBy):
        self.occupiedBy = occupiedBy

    def GetOccupationStatus(self):
        return self.occupiedBy

    def GetNeighbors(self):
        neighbors = [[self.row, self.column-1,],
                     [self.row+1, self.column-1],
                     [self.row-1, self.column],
                     [self.row+1, self.column],
                     [self.row-1, self.column+1],
                     [self.row, self.column+1]]

        for position in neighbors:
            if position[0] < 0 or position[1] < 0 or position[0] >= self.board_size or position[1] >= self.board_size:
                position.clear()

        neighbors = [empty for empty in neighbors if empty]

        return neighbors