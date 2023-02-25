import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
from config import *

colours = ['white', 'green', 'black', 'red', 'purple']
cmap = colors.ListedColormap(colours)

np.random.seed(SEED_VAL)
system = np.random.random([WIDTH, HEIGHT])
system = np.where(system <= TREE_PROB, TREE, EMPTY)
burn_time = np.zeros((WIDTH, HEIGHT))
burn_time[system == TREE] = np.random.randint(MIN_BURN_TIME, MAX_BURN_TIME, size=np.count_nonzero(system == TREE))

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

def start_fire(system):
    trees = np.argwhere(system == TREE)
    initial = trees[random.randint(0, trees.shape[0]-1)]
    system[initial[0], initial[1]] = FIRE

def spread_fire(system):
    new_system = np.copy(system)

    for i in range(WIDTH):
        for j in range(HEIGHT):
            if system[i, j] == FIRE:
                for d in range(3):
                    for x in range(i-d, i+d+1):
                        for y in range(j-d, j+d+1):
                            if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
                                if system[x, y] == TREE and new_system[x, y] != FIRE:
                                    if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                        new_system[x, y] = FIRE
                                        burn_time[x, y] = np.random.randint(MIN_BURN_TIME, MAX_BURN_TIME)
                                elif system[x, y] == BURNT:
                                    new_system[x, y] = BURNT
                                elif system[x, y] == FIRE:
                                    burn_time[x, y] -= 1
                                    if burn_time[x, y] <= 0:
                                        new_system[x, y] = BURNT
                                else:
                                    new_system[x, y] = system[x, y]

    return new_system


make_settlements(system, NUM_SETTLEMENTS, MIN_SETTLE_SIZE, MAX_SETTLE_SIZE)
start_fire(system)

while np.any(system == FIRE):
    system = spread_fire(system)
    plt.imshow(system, cmap=cmap)
    plt.pause(0.001)
plt.show()
