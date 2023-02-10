import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from Position import Position

mpl.use('TkAgg')

class Board:
    def __init__(self, board_size, showPlot):
        self.board_size = board_size
        self.boardPositions = []
        self.showPlot = showPlot

        self.fig = None
        self.ax = None
        self.createBoard()

    def GetBoardSize(self):
        return self.board_size

    def GetBoard(self):
        return self.boardPositions

    def createBoard(self):
        if self.showPlot:
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
                self.boardPositions.append([])
                for j in range(self.board_size):
                    hex = mpatches.RegularPolygon(((i + j / 2) * 1.15, j), numVertices=6, radius=0.64,
                                                  orientation=np.pi, edgecolor='black', facecolor='white')
                    self.ax.add_patch(hex)

                    self.boardPositions[i].append(Position(i, j, hex, None, self.board_size))

            plt.xlim(-2, self.board_size * 1.5 * 1.15 + 1)
            plt.ylim(-2, self.board_size + 1)

        else:
            for i in range(self.board_size):
                self.boardPositions.append([])
                for j in range(self.board_size):
                    self.boardPositions[i].append(Position(i, j, None, None, self.board_size))

    def CheckIfPlayerWon(self, player):
        uncheckedHexes = []
        checkedHexes = []

        for i in range(self.board_size):
            if player.GetId() == 0:
                if self.GetHexByColumnRow(0, i).occupiedBy == player:
                    if self.GetHexByColumnRow(0, i) not in checkedHexes:
                        uncheckedHexes.append(self.GetHexByColumnRow(0, i))
            elif player.GetId() == 1:
                if self.GetHexByColumnRow(i, 0).occupiedBy == player:
                    if self.GetHexByColumnRow(i, 0) not in checkedHexes:
                        uncheckedHexes.append(self.GetHexByColumnRow(i, 0))

        while len(uncheckedHexes) > 0:

            current = uncheckedHexes.pop()
            checkedHexes.append(current)

            if player.GetId() == 0:
                if current.column == self.board_size - 1:
                    return player
            elif player.GetId() == 1:
                if current.row == self.board_size - 1:
                    return player

            for neighbor in current.GetNeighbors():
                try:
                    hex = self.GetHexByColumnRow(neighbor[1], neighbor[0])
                    if hex not in checkedHexes and hex.GetOccupationStatus() == player:
                        uncheckedHexes.append(hex)
                except:  # to be removed
                    print("Exception occured!")
                    continue

    def PlaceAndCheck(self, player, column, row):
        self.boardPositions[column][row].SetOccupationStatus(player)

        if self.showPlot:
            self.GetHexByColumnRow(column, row).GetHex().set_facecolor(player.GetColor())
            plt.plot()

        if self.CheckIfPlayerWon(player):
            print('Game ended: ' + player.GetColor() + ' won!')
            return 1

    def GetHexByColumnRow(self, column, row):
        return self.boardPositions[column][row]