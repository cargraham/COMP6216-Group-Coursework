import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
from config import *


# Initialise the system
def initialise():
    np.random.seed(SEED_VAL)
    system = np.random.random([WIDTH, HEIGHT])
    system = np.where(system <= TREE_PROB, TREE, EMPTY)
    biomass = np.zeros((WIDTH, HEIGHT))

    return system, biomass

def make_break(system, x, y, z):
    x_min, y_min = max(0, x-z), max(0, y-z)
    x_max, y_max = min(len(system[0]-1), x+z), min(len(system)-1, y+z)

    for i in range(x_min, x_max+1):
        for j in range(y_min, y_max+1):
            for w in range(FIREBREAK_WIDTH):
                if (abs(i-x) == z-w or abs(j-y) == z-w) and i >= 0 and i < WIDTH and j >= 0 and j < HEIGHT:
                    system[i, j] = FIRE_BREAK

    return system


# Create random clusters of settlements
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

        system = make_break(system, center[0], center[1], size+2)

    return system


# Pick a random starting point for the fire
def start_fire(system, biomasses):
    trees = np.argwhere(system == TREE)
    initial = trees[random.randint(0, trees.shape[0]-1)]
    system[initial[0], initial[1]] = FIRE
    biomasses[initial[0], initial[1]] = np.random.randint(MIN_BURN_TIME, MAX_BURN_TIME)

    return system, biomasses

# Simulate the spread of the fire
# Iterate through each cell in the system which is on fire
# Iterate through each neighbouring cell with increasing distance
# If the cell is within the bounds of the system, and is a tree which is not on fire:
#   Set the cells state to FIRE from a random chance, given the probability distance
#   Give the burning tree a random burn time
# If the cell is on fire, decrease the burn time by 1. If the new burn time is now < 0, set the state of the cell to BURNT
# Otherwise, keep the cell the same as it was
def spread_fire(system, biomasses):
    new_system = np.copy(system)

    # Iterate through all cells on fire
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if system[i, j] == FIRE:
                #print(f"Cell: {i}, {j}")
                for d in range(len(FIRE_SPREAD_PROBS)):
                    #print(f"d: {d}")
                    x_range = range(max(0, i-d-1), min(WIDTH, i+d+2))
                    #print(f"x_range: {x_range}")
                    y_range = range(max(0, j-d-1), min(HEIGHT, j+d+2))
                    #print(f"y_range: {y_range}")
                    for x in x_range:
                        for y in y_range:
                            if system[x, y] == TREE and new_system[x, y] != FIRE:
                                #print(f"d: {d}. Prob: {FIRE_SPREAD_PROBS[d]}. Cell: {x}, {y}")
                                if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                    new_system[x, y] = FIRE
                                    biomasses[x, y] = np.random.randint(MIN_BURN_TIME, MAX_BURN_TIME)
                            elif system[x, y] == SETTLE and new_system[x, y] != SETTLE_FIRE:
                                if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                    new_system[x, y] = SETTLE_FIRE
                                    biomasses[x, y] = 3
            elif system[i, j] == SETTLE_FIRE:
                for d in range(len(FIRE_SPREAD_PROBS)):
                    x_range = range(max(0, i-d-1), min(WIDTH, i+d+2))
                    y_range = range(max(0, j-d-1), min(HEIGHT, j+d+2))
                    for x in x_range:
                        for y in y_range:
                                if system[x, y] == SETTLE and new_system[x, y] != SETTLE_FIRE:
                                    if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                        new_system[x, y] = SETTLE_FIRE
                                        biomasses[x, y] = 3
                                elif system[x, y] == TREE and new_system[x, y] != FIRE:
                                    if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                        new_system[x, y] = FIRE
                                        biomasses[x, y] = np.random.randint(MIN_BURN_TIME, MAX_BURN_TIME)

    biomasses[biomasses > 0] -= 1
    burn = (system == FIRE) & (biomasses <= 0)
    new_system[burn] = BURNT
    biomasses[burn] = 0
    settle_burn = (system == SETTLE_FIRE) & (biomasses <= 0)
    new_system[settle_burn] = SETTLE_BURNT
    biomasses[settle_burn] = 0

    return new_system, biomasses

def perc_burnt(system):
    burnt = len(np.argwhere(system == BURNT))
    trees = len(np.argwhere(system == TREE))

    settlement = len(np.argwhere(system == SETTLE))
    burnt_settle = len(np.argwhere(system == SETTLE_BURNT))

    print('Burnt trees: ', burnt)
    print('Alive trees: ', trees)
    print(f"Percentage burnt: {burnt / (burnt + trees): .2%}")

    print('\n\nBurnt settlements: ', burnt_settle)
    print('Standing settlements: ', settlement)
    print(f"Percentage burnt: {burnt_settle / (burnt_settle + settlement): .2%}")


# Begin simulation
system, biomass = initialise()
system = make_settlements(system, NUM_SETTLEMENTS, MIN_SETTLE_SIZE, MAX_SETTLE_SIZE)
system, biomass = start_fire(system, biomass)

cmap = colors.ListedColormap(COLORS)
# Continue execution until all fires have burnt
while np.any(system == FIRE):
    system, biomass = spread_fire(system, biomass)
    plt.imshow(system, cmap=cmap)
    plt.pause(0.000001)
    #break

#perc_burnt(system)
plt.show()