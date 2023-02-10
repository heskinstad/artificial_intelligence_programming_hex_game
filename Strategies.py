import random
import matplotlib as mpl
import matplotlib.pyplot as plt

from Board import Board
from Player import Player

class Strategies:
    def __init__(self, grid_size, showPlot):
        self.grid_size = grid_size
        self.showPlot = showPlot


    def PlaceRandomly(self):
        gameBoard = Board(self.grid_size, self.showPlot)

        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        player_won = None

        i = 0
        while i < self.grid_size * self.grid_size:
            random1 = int(random.uniform(0, self.grid_size))
            random2 = int(random.uniform(0, self.grid_size))

            if gameBoard.GetBoard()[random1][random2].GetOccupationStatus() != None:
                continue

            if i % 2:
                if gameBoard.PlaceAndCheck(player0, random1, random2):
                    break
            else:
                if gameBoard.PlaceAndCheck(player1, random1, random2):
                    break

            i += 1

            if self.showPlot:
                plt.pause(0.001)

        if self.showPlot:
            plt.show()