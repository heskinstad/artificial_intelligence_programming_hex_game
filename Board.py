import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from Position import Position

mpl.use('TkAgg')

class Board:
    def __init__(self, board_size, show_plot, initialize=True):
        self.board_size = board_size
        self.board_positions = []
        self.show_plot = show_plot

        self.fig = None
        self.ax = None

        if show_plot:
            self.board_plot = []

        if initialize:
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
            redBorderLeft = mpatches.Rectangle((-1.25, 0), width=1, height=self.board_size * 1.15,
                                               angle=-30, rotation_point='xy', color='red')
            self.ax.add_patch(redBorderLeft)

            redBorderRight = mpatches.Rectangle((-1.25 + self.board_size * 1.15 - 0.2, -0.5), width=1, height=self.board_size * 1.15,
                                                angle=-30, rotation_point='xy', color='red')
            self.ax.add_patch(redBorderRight)

            blueBorderBottom = mpatches.Rectangle((-0.5, 0), width=1, height=self.board_size + 1.5,
                                                  angle=-90, rotation_point='xy', color='blue')
            self.ax.add_patch(blueBorderBottom)

            blueBorderTop = mpatches.Rectangle((-0.3 + self.board_size / 2, self.board_size), width=1, height=self.board_size * 1.2 - 0.6,
                                               angle=-90, rotation_point='xy', color='blue')
            self.ax.add_patch(blueBorderTop)

            # Draw the hexagons
            for y in range(self.board_size):
                self.board_positions.append([])
                self.board_plot.append([])
                for x in range(self.board_size):
                    hex = mpatches.RegularPolygon(((x + y / 2) * 1.15, y), numVertices=6, radius=0.64,
                                                  orientation=np.pi, edgecolor='black', facecolor='white')
                    self.ax.add_patch(hex)

                    self.board_positions[y].append(None)
                    self.board_plot[y].append(hex)

            plt.xlim(-2, self.board_size * 1.5 * 1.15 + 1)
            plt.ylim(-2, self.board_size + 1)

        else:
            for y in range(self.board_size):
                self.board_positions.append([])
                for x in range(self.board_size):
                    self.board_positions[y].append(None)

    def check_if_player_won(self, player):
        unchecked_hexes = []
        checked_hexes = []

        # Check if player has placed any at their 'start edge' - left for red (0), bottom for blue (1)
        # If so, add them to the unchecked_hexes array
        for i in range(self.board_size):
            if self.get_hex_by_x_y(0, i) != None and player.get_id() == 0:
                if self.get_hex_by_x_y(0, i) == player.get_id(): # id 0 move left/right
                    unchecked_hexes.append([0, i])
            elif self.get_hex_by_x_y(i, 0) != None and player.get_id() == 1:
                if self.get_hex_by_x_y(i, 0) == player.get_id(): # id 1 move top/bottom
                    unchecked_hexes.append([i, 0])

        while len(unchecked_hexes) > 0:

            current = unchecked_hexes.pop()
            checked_hexes.append(current)

            if player.get_id() == 0:
                if current[0] == self.board_size - 1:
                    return player
            elif player.get_id() == 1:
                if current[1] == self.board_size - 1:
                    return player

            for neighbor in self.get_neighbors_x_y(current[0], current[1]):
                if [neighbor[0], neighbor[1]] not in checked_hexes and not self.get_hex_by_x_y(neighbor[0], neighbor[1]) == None:
                    if self.get_hex_by_x_y(neighbor[0], neighbor[1]) == player.get_id():
                        unchecked_hexes.append([neighbor[0], neighbor[1]])

    def place(self, player, x, y):
        # Only allow placement if spot is free
        #if self.get_hex_by_x_y(x, y).get_occupation_status() != None:
        #    return 0

        self.set_hex_by_x_y(x, y, player.get_id())

        if self.show_plot:
            self.board_plot[y][x].set_facecolor(player.get_color())
            plt.plot()

        #return 1

    def get_hex_by_x_y(self, x, y):
        return self.board_positions[y][x]

    def set_hex_by_x_y(self, x, y, hex):
        self.board_positions[y][x] = hex

    # Get the neighboring hexes of the position x y
    def get_neighbors(self, x, y):
        neighbors = [[y - 1, x + 1],
                     [y, x + 1],
                     [y - 1, x],
                     [y, x - 1],
                     [y + 1, x],
                     [y + 1, x - 1]]

        # Remove neighbor positions outside the board
        for position in neighbors:
            if position[0] < 0 or position[1] < 0 or position[0] >= self.get_board_size() or position[1] >= self.get_board_size():
                position.clear()

        neighbors = [empty for empty in neighbors if empty]

        return neighbors

    def get_neighbors_x_y(self, x, y):
        neighbors = self.get_neighbors(x, y)

        for position in neighbors:
            temp = position[0]
            position[0] = position[1]
            position[1] = temp

        return neighbors

    def print_board(self):
        for j in range(self.get_board_size()-1, -1, -1):
            print(j * " ", end=' ')
            for i in range(self.get_board_size()):
                if self.get_hex_by_x_y(i, j) == None:
                    print('N', end=' ')
                else:
                    print(self.get_hex_by_x_y(i, j), end=' ')
            print()