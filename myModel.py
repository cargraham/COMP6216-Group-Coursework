import numpy as np

width, height = 100, 100
tree_prob = 0.6

EMPTY, TREE, FIRE, BREAK, SETTLE = 0, 1, 2, 3, 4

np.random.seed(2)
system = np.random.random([width, height])

system = np.where(system <= 0.6, 1, 0)

print(system)

np.savetxt('system.txt', system, fmt='%.1i')
        