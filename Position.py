class Position:
    def __init__(self, column, row, hex, occupied_by, board_size):
        self.row = row
        self.column = column
        self.hex = hex
        self.occupied_by = occupied_by
        self.board_size = board_size

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_coordinates(self):
        return str([self.column, self.row])

    def get_hex(self):
        return self.hex

    def set_occupation_status(self, occupied_by):
        self.occupied_by = occupied_by

    def get_occupation_status(self):
        return self.occupied_by

    def get_neighbors(self):
        neighbors = [[self.row, self.column-1],
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