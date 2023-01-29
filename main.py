import matplotlib.pyplot as plt
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



hexArray = []

# Draw the hexagons
for i in range(grid_size):
    hexArray.append([])
    for j in range(grid_size):
        hex = mpatches.RegularPolygon(((i+j/2)*1.15, j), numVertices=6, radius=0.64,
                                      orientation=np.pi, edgecolor='black',facecolor='white')
        ax.add_patch(hex)

        hexArray[i].append(Position(i, j, hex, grid_size))

for position in hexArray[0][0].GetNeighbors():
    hexArray[position[0]][position[1]].GetHex().set_facecolor('blue')

#hexArray[1][1].set_facecolor('blue')

plt.xlim(-2, grid_size*1.5*1.15+1)
plt.ylim(-2, grid_size+1)
plt.show()