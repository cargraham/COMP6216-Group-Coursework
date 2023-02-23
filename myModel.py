import numpy as np

width, height = 100, 100
tree_prob = 0.6

EMPTY, TREE, FIRE, BREAK, SETTLE = 0, 1, 2, 3, 4

np.random.seed(2)
system = np.random.random([width, height])

system[system <= 0.6] = 1
system[(system > 0.6) and (system != 1)] = 0

print(system)

# for x in range(width):
#     for y in range(height):
#         if(rand_system[x][y] < tree_prob):
#             system[x][y] = 1
        

#print(system)

# np.savetxt('system.txt', system)
        