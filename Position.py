class Position:
    def __init__(self, row, column, hex, occupiedBy, board_size):
        self.row = row
        self.column = column
        self.hex = hex
        self.occupiedBy = occupiedBy
        self.board_size = board_size
        self.h = None

    def GetRow(self):
        return self.row

    def GetColumn(self):
        return self.column

    def GetHex(self):
        return self.hex

    def GetH(self):
        return self.h

    def SetOccupationStatus(self, occupiedBy):
        self.occupiedBy = occupiedBy
        if occupiedBy == 'red':
            self.h = self.board_size - self.column
        elif occupiedBy == 'blue':
            self.h = self.board_size - self.row

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
            if position[0] < 0 or position[1] < 0 or position[0] > self.board_size or position[1] > self.board_size:
                position.clear()

        neighbors = [empty for empty in neighbors if empty]

        return neighbors