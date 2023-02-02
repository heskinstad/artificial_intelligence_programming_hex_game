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
gameBoard = Board(grid_size)

fig, ax = plt.subplots(figsize=(7,7))

# Set the aspect ratio to match the hexagons
ax.set_aspect('equal', adjustable='box')

# Remove axis labels and ticks
ax.axis('off')

# Draw red/blue edges
redBorderLeft = mpatches.Rectangle((-1.25, 0),width=1,height=grid_size*1.15,angle=-30,rotation_point='xy', color='red')
ax.add_patch(redBorderLeft)

redBorderRight = mpatches.Rectangle((-1.25+grid_size*1.15-0.2, -0.5),width=1,height=grid_size*1.15,angle=-30,rotation_point='xy', color='red')
ax.add_patch(redBorderRight)

blueBorderBottom = mpatches.Rectangle((-0.5, 0),width=1,height=grid_size+1.5,angle=-90,rotation_point='xy', color='blue')
ax.add_patch(blueBorderBottom)

blueBorderTop = mpatches.Rectangle((-0.3+grid_size/2, grid_size),width=1,height=grid_size*1.2-0.6,angle=-90,rotation_point='xy', color='blue')
ax.add_patch(blueBorderTop)

def GetHexByColumnRow(array, column, row):
    return array[column][row]

hexArray = []

player0 = Player(0, 'red')
player1 = Player(1, 'blue')

player_won = None

# Draw the hexagons
for i in range(grid_size):
    hexArray.append([])
    for j in range(grid_size):
        hex = mpatches.RegularPolygon(((i+j/2)*1.15, j), numVertices=6, radius=0.64,
                                      orientation=np.pi, edgecolor='black',facecolor='white')
        ax.add_patch(hex)

        hexArray[i].append(Position(i, j, hex, None, grid_size))

plt.xlim(-2, grid_size*1.5*1.15+1)
plt.ylim(-2, grid_size+1)

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
                if hex not in checkedHexes and hex.occupiedBy == player:
                    uncheckedHexes.append(hex)
            except:
                continue

def PlaceAndCheck(player, column, row):
    hexArray[column][row].SetOccupationStatus(player)
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
    plt.pause(0.01)



plt.show()