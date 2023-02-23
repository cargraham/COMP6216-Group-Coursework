import random, sys, time, bext
import matplotlib.pyplot as plt

width = 30
height = 10

tree = '1'
fire = '2'
empty = '0'

initial_tree_density = 0.7
grow_chance = 0.2
fire_chance = 0.01

pause_length = 0.5

def main():
    forest = createForest()
    bext.clear()

    while True:
        displayForest(forest)

        nextForest = {'width': forest['width'], 'height': forest['height']}
        
        forest = iteration(forest, nextForest)

        time.sleep(pause_length)

def iteration(oldForest, newForest):
    for x in range(oldForest['width']):
            for y in range(oldForest['height']):
                if(x, y) in newForest:
                    continue
                if((oldForest[(x, y)] == empty) and (random.random() <= grow_chance)):
                    newForest[(x, y)] = tree
                elif((oldForest[(x, y)] == tree) and (random.random() <= fire_chance)):
                    newForest[(x, y)] = fire
                elif oldForest[(x, y)] == fire:
                    for ix in range(-1, 2):
                        for iy in range(-1, 2):
                            if oldForest.get((x + ix, y + iy)) == tree:
                                newForest[(x + ix, y + iy)] = fire
                    newForest[(x, y)] = empty
                else:
                    newForest[(x, y)] = oldForest[(x, y)]

    return newForest
    

def createForest():
    forest = {'width': width, 'height': height}
    for x in range(width):
        for y in range(height):
            if(random.random() * 100) <= initial_tree_density:
                forest[(x, y)] = tree
            else:
                forest[(x, y)] = empty
    return forest

def displayForest(forest):
    bext.goto(0, 0)
    for y in range(forest['height']):
        for x in range(forest['width']):
            if forest[(x, y)] == tree:
                bext.fg('green')
                print(tree, end='')
            elif forest[(x, y)] == fire:
                bext.fg('red')
                print(fire, end='')
            elif forest[(x, y)] == empty:
                bext.fg('black')
                print(empty, end='')
        print()
    bext.fg('reset')
    print('Grow Chance: {}% '.format(grow_chance * 100), end='')
    print('Lightning Chance: {}% '.format(fire_chance * 100), end='')
    print('\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()