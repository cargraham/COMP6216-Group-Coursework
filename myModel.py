import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math

width, height = 100, 100
tree_prob = 0.6
settle_prob = 0.6
settle_num = 5
neighbours = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
              (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
              (-2, 0), (-1, 0), (1, 0), (2, 0),
              (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
              (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]

EMPTY, TREE, SETTLE, FIRE, BREAK,  = 0, 1, 2, 3, 4

colours = ['white', 'green', 'brown']
            # 'orange', 'black']
cmap = colors.ListedColormap(colours)

np.random.seed(2)
system = np.random.random([width, height])

system = np.where(system <= tree_prob, TREE, EMPTY)

def settle_neighbours(x, y):
    system[x][y] = SETTLE
    for n in neighbours:
        neigh_x = x + n[0]
        neigh_y = y + n[1]
        if((neigh_x >= 0 and neigh_x < width) and (neigh_y >= 0 and neigh_y < height)):
            if(np.random.random() <= settle_prob):
                system[neigh_x][neigh_y] = SETTLE

# generate settlements
for settle in range(settle_num):
    x = math.trunc(np.random.random() * 100)
    y = math.trunc(np.random.random() * 100)
    settle_neighbours(x, y)

plt.imshow(system, cmap=cmap)
plt.show()

# print(system)

np.savetxt('system.txt', system, fmt='%.1i')
        