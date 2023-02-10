import random
import matplotlib as mpl
import matplotlib.pyplot as plt

from Board import Board
from Player import Player

mpl.use('TkAgg')
import matplotlib.patches as mpatches
import numpy as np

from Position import Position

grid_size = 11
showPlot = True
gameBoard = Board(grid_size, showPlot)

def GetHexByColumnRow(array, column, row):
    return array[column][row]

hexArray = gameBoard.GetBoard()

player0 = Player(0, 'red')
player1 = Player(1, 'blue')

player_won = None

def CheckIfPlayerWon(player):
    uncheckedHexes = []
    checkedHexes = []

    for i in range(grid_size):
        if player.GetId() == 0:
            if GetHexByColumnRow(hexArray, 0, i).occupiedBy == player:
                if GetHexByColumnRow(hexArray, 0, i) not in checkedHexes:
                    uncheckedHexes.append(GetHexByColumnRow(hexArray, 0, i))
        elif player.GetId() == 1:
            if GetHexByColumnRow(hexArray, i, 0).occupiedBy == player:
                if GetHexByColumnRow(hexArray, i, 0) not in checkedHexes:
                    uncheckedHexes.append(GetHexByColumnRow(hexArray, i, 0))

    while len(uncheckedHexes) > 0:

        current = uncheckedHexes.pop()
        checkedHexes.append(current)

        if player.GetId() == 0:
            if current.column == grid_size-1:
                return player
        elif player.GetId() == 1:
            if current.row == grid_size-1:
                return player

        for neighbor in current.GetNeighbors():
            try:
                hex = GetHexByColumnRow(hexArray, neighbor[1], neighbor[0])
                if hex not in checkedHexes and hex.GetOccupationStatus() == player:
                    uncheckedHexes.append(hex)
            except:
                continue

def PlaceAndCheck(player, column, row):
    hexArray[column][row].SetOccupationStatus(player)

    if showPlot:
        hexArray[column][row].GetHex().set_facecolor(player.GetColor())
        plt.plot()

    if CheckIfPlayerWon(player):
        print('Game ended: ' + player.GetColor() + ' won!')
        return 1

i = 0
while i < grid_size*grid_size:
    random1 = int(random.uniform(0, grid_size))
    random2 = int(random.uniform(0, grid_size))

    if hexArray[random1][random2].GetOccupationStatus() != None:
        continue

    if i % 2:
        if PlaceAndCheck(player0, random1, random2):
            break
    else:
        if PlaceAndCheck(player1, random1, random2):
            break

    i += 1

    if showPlot:
        plt.pause(0.001)


if showPlot:
    plt.show()