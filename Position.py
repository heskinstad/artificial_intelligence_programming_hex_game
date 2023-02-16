class Position:
    def __init__(self, x, y, hex, occupied_by, board_size):
        self.y = y
        self.x = x
        self.hex = hex
        self.occupied_by = occupied_by
        self.board_size = board_size

    def get_row(self):
        return self.y

    def get_column(self):
        return self.x

    def get_coordinates(self):
        return str([self.x, self.y])

    def get_hex(self):
        return self.hex

    def set_occupation_status(self, occupied_by):
        self.occupied_by = occupied_by

    def get_occupation_status(self):
        return self.occupied_by

    def get_neighbors(self):
        neighbors = [[self.y, self.x - 1],
                     [self.y + 1, self.x - 1],
                     [self.y - 1, self.x],
                     [self.y + 1, self.x],
                     [self.y - 1, self.x + 1],
                     [self.y, self.x + 1]]

        for position in neighbors:
            if position[0] < 0 or position[1] < 0 or position[0] >= self.board_size or position[1] >= self.board_size:
                position.clear()

        neighbors = [empty for empty in neighbors if empty]

        return neighbors