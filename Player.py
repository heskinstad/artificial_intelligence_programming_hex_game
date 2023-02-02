class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color

    def GetId(self):
        return int(self.id)

    def GetColor(self):
        return str(self.color)