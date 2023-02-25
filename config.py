SEED_VAL = 1    # Seed value for the random generator (repeatable results)
WIDTH, HEIGHT = 100, 100    # Size of the system
TREE_PROB = 0.6     # Density of the forest
NUM_SETTLEMENTS = 5     # Number of settlement clusters
MIN_SETTLE_SIZE = 5     # Minimum size of a settlement
MAX_SETTLE_SIZE = 10    # Maximum size of a settlement
FIRE_SPREAD_PROBS = [0.8, 0.5, 0.2]     # Probability that a fire will spread to a neigbouring tree, (index+1) in array corresponds to distance away from burning tree
MIN_BURN_TIME = 3       # Minimum time a tree should burn for
MAX_BURN_TIME = 8       # Maximum time a tree should burn for 

EMPTY, TREE, SETTLE, FIRE, BURNT = 0, 1, 2, 3, 5    # Values corresponding to each state
COLORS = ['white', 'green', 'black', 'red', 'purple']   # Color for each state
