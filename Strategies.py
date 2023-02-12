import random
import matplotlib.pyplot as plt

from Board import Board
from Player import Player

class Strategies:
    def __init__(self, grid_size, show_plot):
        self.grid_size = grid_size
        self.show_plot = show_plot


    def place_randomly(self):
        gameBoard = Board(self.grid_size, self.show_plot)

        player0 = Player(0, 'red')
        player1 = Player(1, 'blue')

        i = 0
        while i < self.grid_size * self.grid_size:
            random1 = int(random.uniform(0, self.grid_size))
            random2 = int(random.uniform(0, self.grid_size))

            if gameBoard.get_board()[random1][random2].get_occupation_status() != None:
                continue

            if i % 2:
                gameBoard.place(player0, random1, random2)
                if gameBoard.check_if_player_won(player0):
                    print('Game ended: ' + player0.get_color() + ' won!')
                    break
            else:
                gameBoard.place(player1, random1, random2)
                if gameBoard.check_if_player_won(player1):
                    print('Game ended: ' + player1.get_color() + ' won!')
                    break

            i += 1

            if self.show_plot:
                plt.pause(0.001)

        if self.show_plot:
            plt.show()