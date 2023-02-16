class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.tete = 1

    def get_id(self):
        return int(self.id)

    def get_color(self):
        return str(self.color)

    def get_tete(self):
        return 1