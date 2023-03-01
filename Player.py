class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color

    def get_id(self):
        return int(self.id)

    def get_color(self):
        return str(self.color)