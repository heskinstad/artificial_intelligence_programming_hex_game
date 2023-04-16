class Player:
    def __init__(self, id, color, direction=None):
        self.id = id
        self.color = color
        self.direction = direction

    def get_id(self):
        return int(self.id)

    def get_color(self):
        return str(self.color)

    def get_direction(self):
        return str(self.direction)

    def set_direction(self, direction):
        self.direction = direction