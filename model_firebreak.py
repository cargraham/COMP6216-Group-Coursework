import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
from config import *
import pandas as pd
import json


def prog(SEED_VAL, FIREBREAK_WIDTH):

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

    def make_water_station(system, x, y, z):
        system[x, y] = WATER_STATION
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

            #system = make_water_station(system, center[0], center[1], size+5)    
            system = make_break(system, center[0], center[1], size+2)

        return system


    # Pick a random starting point for the fire
    def start_fire(system, biomasses):
        trees = np.argwhere(system == TREE)
        initial = trees[random.randint(0, trees.shape[0]-1)]
        system[initial[0], initial[1]] = FIRE
        biomasses[initial[0], initial[1]] = np.random.randint(MIN_BIOMASS, MAX_BIOMASS)

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

        fire_bool = np.logical_or(system == FIRE, system == SETTLE_FIRE)

        fires = np.argwhere(fire_bool)
        for i, j in fires:
            for d in range(len(FIRE_SPREAD_PROBS)):
                x_range = range(max(0, i-d-1), min(WIDTH, i+d+2))
                y_range = range(max(0, j-d-1), min(HEIGHT, j+d+2))
                for x in x_range:
                    for y in y_range:
                        if system[x, y] == TREE and new_system[x, y] != FIRE:
                            if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                new_system[x, y] = FIRE
                                biomasses[x, y] = np.random.randint(MIN_BIOMASS, MAX_BIOMASS)
                        elif system[x, y] == SETTLE and new_system[x, y] != SETTLE_FIRE:
                            if np.random.random() <= FIRE_SPREAD_PROBS[d]:
                                new_system[x, y] = SETTLE_FIRE
                                biomasses[x, y] = 3
        

        biomasses[biomasses > 0] -= 1
        burn = (system == FIRE) & (biomasses <= 0)
        new_system[burn] = BURNT
        biomasses[burn] = 0
        settle_burn = (system == SETTLE_FIRE) & (biomasses <= 0)
        new_system[settle_burn] = SETTLE_BURNT
        biomasses[settle_burn] = 0

        return new_system, biomasses

    def water_station(system, new_system, i, j):
        for d in range(1, STATION_RADIUS):
            x_range = range(max(0, i-d-1), min(WIDTH, i+d+2))
            y_range = range(max(0, j-d)-1, min(HEIGHT, j+d+2))

            for x in x_range:
                for y in y_range:
                    if system[x, y] == FIRE and new_system[x, y] != WET_TREE:
                        new_system[x, y] = WET_TREE
                        return new_system
                    elif system[x, y] == SETTLE_FIRE and new_system[x, y] != WET_SETTLE:
                        new_system[x, y] = WET_SETTLE
                        return new_system
        return new_system

    def water_fires(system):
        new_system = np.copy(system)

        stations = np.argwhere(system == WATER_STATION)
        for i, j in stations:
            for _ in range(STATION_POWER):
                new_system = water_station(system, new_system, i, j)

        return new_system

    def perc_burnt(system):
        burnt = len(np.argwhere(system == BURNT))
        trees = len(np.argwhere(system == TREE))
        wet_trees = len(np.argwhere(system == WET_TREE))

        settlement = len(np.argwhere(system == SETTLE))
        burnt_settle = len(np.argwhere(system == SETTLE_BURNT))
        wet_settlement = len(np.argwhere(system == WET_SETTLE))

        print('Burnt trees: ', burnt)
        print('Alive trees: ', trees)
        print(f"Wet trees: {wet_trees}")
        print(f"Percentage burnt: {burnt / (burnt + wet_trees + trees): .2%}")

        print('\n\nBurnt settlements: ', burnt_settle)
        print('Standing settlements: ', settlement)
        print(f"Wet settlements: {wet_settlement}")
        print(f"Percentage burnt: {burnt_settle / (burnt_settle + wet_settlement + settlement): .2%}")


    # Begin simulation
    system, biomass = initialise()
    system = make_settlements(system, NUM_SETTLEMENTS, MIN_SETTLE_SIZE, MAX_SETTLE_SIZE)
    system, biomass = start_fire(system, biomass)


    cmap = colors.ListedColormap(COLORS)
    cmap.set_under('gray', alpha=0)

    bounds = [value-0.5 for value in VALUES] + [VALUES[-1]+0.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)# Continue execution until all fires have burnt

    df = pd.DataFrame(columns=['burnt', 'trees', 'wet_trees', 'settlement', 'burnt_settle', 'wet_settlement', 'perc_burnt', 'perc_settle_burnt'])

    while np.any(system == FIRE):
        burnt = len(np.argwhere(system == BURNT))
        trees = len(np.argwhere(system == TREE))
        wet_trees = len(np.argwhere(system == WET_TREE))

        settlement = len(np.argwhere(system == SETTLE))
        burnt_settle = len(np.argwhere(system == SETTLE_BURNT))
        wet_settlement = len(np.argwhere(system == WET_SETTLE))

        new_row = pd.Series([burnt, trees, wet_trees, settlement, burnt_settle, wet_settlement, burnt / (burnt + wet_trees + trees), burnt_settle / (burnt_settle + wet_settlement + settlement)], index=df.columns)
        df = df.append(new_row, ignore_index=True)

        system = water_fires(system)
        system, biomass = spread_fire(system, biomass)
        #plt.imshow(system, cmap=cmap, norm=norm)
        #plt.pause(0.00000001)
        #break

    plt.imshow(system, cmap=cmap, norm=norm)
    plt.show()
    return df


    #perc_burnt(system)
    #plt.show()

prog(2)

for width in range(1, 4):
    with pd.ExcelWriter(f"firebreak_results_{width}.xlsx") as writer:
        for seed in range(5):
            df = prog(seed, width)
            df.to_excel(writer, sheet_name=(f"FIREBREAK_{seed}"))
