import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random

SEED_VAL = 1
WIDTH, HEIGHT = 100, 100
TREE_PROB = 0.6
NUM_SETTLEMENTS = 5
MIN_SETTLE_SIZE = 5
MAX_SETTLE_SIZE = 10

EMPTY, TREE, SETTLE, FIRE, BREAK = 0, 1, 2, 3, 4

colours = ['white', 'green', 'brown']
cmap = colors.ListedColormap(colours)

np.random.seed(SEED_VAL)
system = np.random.random([WIDTH, HEIGHT])
system = np.where(system <= TREE_PROB, TREE, EMPTY)

def make_settlements(system, num, min_size, max_size):
    for i in range(num):
        random.seed(SEED_VAL + i+1)
        size = random.randint(min_size, max_size)
        center = (random.randint(size, system.shape[0]-size-1), random.randint(size, system.shape[1]-size-1))

        shape_size = size if size % 2 == 1 else size + 1
        np.random.seed(SEED_VAL + i+1)
        shape = np.random.choice([0, 1], size=(shape_size, shape_size), p=[0.4, 0.6])

        x1, y1 = center[0] - shape_size//2, center[1] - shape_size//2
        x2, y2 = center[0] + shape_size//2, center[1] + shape_size//2
        system[x1:x2+1, y1:y2+1][shape==1] = SETTLE

make_settlements(system, NUM_SETTLEMENTS, MIN_SETTLE_SIZE, MAX_SETTLE_SIZE)

plt.imshow(system, cmap=cmap)
plt.show()

np.savetxt('system.txt', system, fmt='%.1i')