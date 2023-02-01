import random
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('TkAgg')
import matplotlib.patches as mpatches
import numpy as np

from Position import Position

grid_size = 11

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
redHexes = []
blueHexes = []

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
        if player == 'red':
            if GetHexByColumnRow(hexArray, 0, i).occupiedBy == player:
                if GetHexByColumnRow(hexArray, 0, i) not in checkedHexes:
                    uncheckedHexes.append(GetHexByColumnRow(hexArray, 0, i))
        elif player == 'blue':
            if GetHexByColumnRow(hexArray, i, 0).occupiedBy == player:
                if GetHexByColumnRow(hexArray, i, 0) not in checkedHexes:
                    uncheckedHexes.append(GetHexByColumnRow(hexArray, i, 0))

    while len(uncheckedHexes) > 0:

        current = uncheckedHexes.pop()
        checkedHexes.append(current)

        if player == 'red':
            if current.column == grid_size-1:
                return 1
        elif player == 'blue':
            if current.row == grid_size-1:
                return 1

        for neighbor in current.GetNeighbors():
            try:
                hex = GetHexByColumnRow(hexArray, neighbor[1], neighbor[0])
                if hex not in checkedHexes and hex.occupiedBy == player:
                    uncheckedHexes.append(hex)
            except:
                continue

i = 0
while i < grid_size*grid_size:
    random1 = int(random.uniform(0, grid_size))
    random2 = int(random.uniform(0, grid_size))
    if hexArray[random1][random2].GetOccupationStatus() != None:
        continue
    if i % 2:
        hexArray[random1][random2].GetHex().set_facecolor('blue')
        hexArray[random1][random2].SetOccupationStatus('blue')
        blueHexes.append(hexArray[random1][random2])
    else:
        hexArray[random1][random2].GetHex().set_facecolor('red')
        hexArray[random1][random2].SetOccupationStatus('red')
        redHexes.append(hexArray[random1][random2])

    plt.plot()

    if CheckIfPlayerWon('red'):
        print('Game ended: red won!')
        break
    elif CheckIfPlayerWon('blue'):
        print('Game ended: blue won!')
        break
    elif i == grid_size * grid_size:
        print('Game ended: No free spaces left.')

    i += 1
    plt.pause(0.01)

plt.show()