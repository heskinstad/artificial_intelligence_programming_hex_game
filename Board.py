import copy

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

mpl.use('TkAgg')

class Board:
    def __init__(self, board_size, initialize=True):
        self.board_size = board_size
        self.board_positions = []
        self.board_plot = []

        self.fig = None
        self.ax = None

        if initialize:
            self.create_board()

    def get_board_size(self):
        return self.board_size

    def get_board_p1(self):
        return self.board_positions

    def get_board_p2(self):
        return self.board_positions

    def get_board_np(self):
        board = np.array(copy.deepcopy(self.board_positions))

        return np.array(board)

    def get_board_np_p1(self):
        board = np.array(self.get_board_p1())

        p1_board = np.where(board == 1, 1, 0)

        return np.array(p1_board, dtype=np.int)

    def get_board_np_p2(self):
        board = np.array(self.get_board_p2())

        p2_board = np.where(board == 2, 1, 0)

        return np.array(p2_board, dtype=np.int)


    def create_board(self):
        for y in range(self.board_size):
            self.board_positions.append([])
            for x in range(self.board_size):
                self.board_positions[y].append(0)

    def get_fig(self):
        return self.fig

    def get_ax(self):
        return self.ax

    def initialize_board_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(self.get_board_size(), self.get_board_size()))

    def create_board_plot(self, fig, ax):
        self.fig = fig
        self.ax = ax

        # Set the aspect ratio to match the hexagons
        self.ax.set_aspect('equal', adjustable='box')

        # Remove axis labels and ticks
        self.ax.axis('off')

        # Draw red/blue edges
        redBorderLeft = mpatches.Rectangle((-1.25, 0), width=1, height=self.board_size * 1.15,
                                           angle=-30, rotation_point='xy', color='red')
        self.ax.add_patch(redBorderLeft)

        redBorderRight = mpatches.Rectangle((-1.25 + self.board_size * 1.15 - 0.2, -0.5), width=1,
                                            height=self.board_size * 1.15,
                                            angle=-30, rotation_point='xy', color='red')
        self.ax.add_patch(redBorderRight)

        blueBorderBottom = mpatches.Rectangle((-0.5, 0), width=1, height=self.board_size + 1.5,
                                              angle=-90, rotation_point='xy', color='blue')
        self.ax.add_patch(blueBorderBottom)

        blueBorderTop = mpatches.Rectangle((-0.3 + self.board_size / 2, self.board_size), width=1,
                                           height=self.board_size * 1.2 - 0.6,
                                           angle=-90, rotation_point='xy', color='blue')
        self.ax.add_patch(blueBorderTop)

        # Draw the hexagons
        for y in range(self.board_size):
            self.board_positions.append([])
            self.board_plot.append([])
            for x in range(self.board_size):
                if self.get_board_p1()[y][x] == 0:
                    hex = mpatches.RegularPolygon(((x + y / 2) * 1.15, y), numVertices=6, radius=0.64,
                                                orientation=np.pi, edgecolor='black', facecolor='white')
                elif self.get_board_p1()[y][x] == 1:
                    hex = mpatches.RegularPolygon(((x + y / 2) * 1.15, y), numVertices=6, radius=0.64,
                                                orientation=np.pi, edgecolor='black', facecolor='red')
                elif self.get_board_p1()[y][x] == 2:
                    hex = mpatches.RegularPolygon(((x + y / 2) * 1.15, y), numVertices=6, radius=0.64,
                                                orientation=np.pi, edgecolor='black', facecolor='blue')

                self.ax.add_patch(hex)

                self.board_positions[y].append(self.get_board_p1()[y][x])
                self.board_plot[y].append(hex)

        plt.xlim(-2, self.board_size * 1.5 * 1.15 + 1)
        plt.ylim(-2, self.board_size + 1)

        plt.plot()

    # Check if the player sent in as the first argument has won
    def check_if_player_won(self, player, starting_player, second_player):
        unchecked_hexes = []
        checked_hexes = []

        # Check if player has placed any at their 'start edge' - left for red (0), bottom for blue (1)
        # If so, add them to the unchecked_hexes array
        for i in range(self.board_size):
            if player.get_id() == 1:
                if self.get_hex_by_x_y(0, i) == player.get_id(): # id 1 move left/right
                    unchecked_hexes.append([0, i])
            elif player.get_id() == 2:
                if self.get_hex_by_x_y(i, 0) == player.get_id(): # id 2 move top/bottom
                    unchecked_hexes.append([i, 0])

        while len(unchecked_hexes) > 0:

            current = unchecked_hexes.pop()
            checked_hexes.append(current)

            if player.get_id() == 1:
                if current[0] == self.board_size - 1:
                    return player
            elif player.get_id() == 2:
                if current[1] == self.board_size - 1:
                    return player

            for neighbor in self.get_neighbors_x_y(current[0], current[1]):
                if [neighbor[0], neighbor[1]] not in checked_hexes:
                    if self.get_hex_by_x_y(neighbor[0], neighbor[1]) == player.get_id():
                        unchecked_hexes.append([neighbor[0], neighbor[1]])


    def place(self, player, x, y):
        self.set_hex_by_x_y(x, y, player.get_id())

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


    # Print the board to the console
    def print_board(self):
        print(self.get_board_size() * " " + self.get_board_size() * 2 * "_" + "__")
        for j in range(self.get_board_size()-1, -1, -1):
            print(j * " ", end='/ ')
            for i in range(self.get_board_size()):
                if self.get_hex_by_x_y(i, j) == 0:
                    print(' ', end=' ')
                else:
                    print(self.get_hex_by_x_y(i, j), end=' ')
            print("/")
        print(self.get_board_size() * 2 * "¯" + "¯¯")