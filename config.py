SEED_VAL = 0    # Seed value for the random generator (repeatable results)
WIDTH, HEIGHT = 100, 100    # Size of the system
TREE_PROB = 0.6         # Density of the forest
NUM_SETTLEMENTS = 5     # Number of settlement clusters
MIN_SETTLE_SIZE = 5     # Minimum size of a settlement
MAX_SETTLE_SIZE = 10    # Maximum size of a settlement
FIRE_SPREAD_PROBS = [0.8, 0.5, 0.02]     # Probability that a fire will spread to a neigbouring tree, (index+1) in array corresponds to distance away from burning tree
MIN_BURN_TIME = 1       # Minimum time a tree should burn for
MAX_BURN_TIME = 8       # Maximum time a tree should burn for
FIREBREAK_WIDTH = 2     # Width of the fire break

EMPTY, TREE, FIRE, BURNT, SETTLE, SETTLE_FIRE, SETTLE_BURNT, FIRE_BREAK = 0, 1, 2, 3, 4, 5, 6, 7    # Values corresponding to each state
COLORS = ['white', 'green', 'red', 'black', 'purple', 'red', 'gray', 'blue']   # Color for each state


# Watering:
# Supress / reduce FIRE_SPREAD_PROBS in watered zone

# Firebreak:
# Remove trees in area

# Fuelbreak:
# Reduce biomass in area

# Controlled burns ???
