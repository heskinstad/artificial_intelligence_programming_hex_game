import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from Position import Position

mpl.use('TkAgg')

class Board:
    def __init__(self, board_size, show_plot):
        self.board_size = board_size
        self.board_positions = []
        self.show_plot = show_plot

        self.fig = None
        self.ax = None
        self.create_board()

    def get_board_size(self):
        return self.board_size

    def get_board(self):
        return self.board_positions

    def create_board(self):
        if self.show_plot:
            self.fig, self.ax = plt.subplots(figsize=(7, 7))

            # Set the aspect ratio to match the hexagons
            self.ax.set_aspect('equal', adjustable='box')

            # Remove axis labels and ticks
            self.ax.axis('off')

            # Draw red/blue edges
            redBorderLeft = mpatches.Rectangle((-1.25, 0), width=1, height=self.board_size * 1.15, angle=-30,
                                               rotation_point='xy',
                                               color='red')
            self.ax.add_patch(redBorderLeft)

            redBorderRight = mpatches.Rectangle((-1.25 + self.board_size * 1.15 - 0.2, -0.5), width=1,
                                                height=self.board_size * 1.15,
                                                angle=-30, rotation_point='xy', color='red')
            self.ax.add_patch(redBorderRight)

            blueBorderBottom = mpatches.Rectangle((-0.5, 0), width=1, height=self.board_size + 1.5, angle=-90,
                                                  rotation_point='xy',
                                                  color='blue')
            self.ax.add_patch(blueBorderBottom)

            blueBorderTop = mpatches.Rectangle((-0.3 + self.board_size / 2, self.board_size), width=1, height=self.board_size * 1.2 - 0.6,
                                               angle=-90, rotation_point='xy', color='blue')
            self.ax.add_patch(blueBorderTop)

            # Draw the hexagons
            for i in range(self.board_size):
                self.board_positions.append([])
                for j in range(self.board_size):
                    hex = mpatches.RegularPolygon(((i + j / 2) * 1.15, j), numVertices=6, radius=0.64,
                                                  orientation=np.pi, edgecolor='black', facecolor='white')
                    self.ax.add_patch(hex)

                    self.board_positions[i].append(Position(i, j, hex, None, self.board_size))

            plt.xlim(-2, self.board_size * 1.5 * 1.15 + 1)
            plt.ylim(-2, self.board_size + 1)

        else:
            for i in range(self.board_size):
                self.board_positions.append([])
                for j in range(self.board_size):
                    self.board_positions[i].append(Position(i, j, None, None, self.board_size))

    def check_if_player_won(self, player):
        unchecked_hexes = []
        checked_hexes = []

        for i in range(self.board_size):
            if player.get_id() == 0:
                if self.get_hex_by_column_row(0, i).occupied_by == player:
                    if self.get_hex_by_column_row(0, i) not in checked_hexes:
                        unchecked_hexes.append(self.get_hex_by_column_row(0, i))
            elif player.get_id() == 1:
                if self.get_hex_by_column_row(i, 0).occupied_by == player:
                    if self.get_hex_by_column_row(i, 0) not in checked_hexes:
                        unchecked_hexes.append(self.get_hex_by_column_row(i, 0))

        while len(unchecked_hexes) > 0:

            current = unchecked_hexes.pop()
            checked_hexes.append(current)

            if player.get_id() == 0:
                if current.column == self.board_size - 1:
                    print("AAAAA")
                    return player
            elif player.get_id() == 1:
                if current.row == self.board_size - 1:
                    print("AAAAA")
                    return player

            for neighbor in current.get_neighbors():
                try:
                    hex = self.get_hex_by_column_row(neighbor[1], neighbor[0])
                    if hex not in checked_hexes and hex.get_occupation_status() == player:
                        unchecked_hexes.append(hex)
                except:  # to be removed
                    print("Exception occured!")
                    continue

    def place(self, player, column, row):
        self.board_positions[column][row].set_occupation_status(player)

        if self.show_plot:
            self.get_hex_by_column_row(column, row).get_hex().set_facecolor(player.get_color())
            plt.plot()

    def get_hex_by_column_row(self, column, row):
        return self.board_positions[column][row]

    def set_hex_by_column_row(self, column, row, hex):
        self.board_positions[column][row] = hex

    def print_board(self):
        for i in range(self.get_board_size()):
            for j in range(self.get_board_size()):
                if self.get_hex_by_column_row(i, j).get_occupation_status() == None:
                    print('None', end=' ')
                else:
                    print(self.get_hex_by_column_row(i, j).get_occupation_status().get_color(), end=' ')
            print()
        print()