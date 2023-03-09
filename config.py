SEED_VAL = 0    # Seed value for the random generator (repeatable results)
WIDTH, HEIGHT = 100, 100    # Size of the system
TREE_PROB = 0.6         # Density of the forest
NUM_SETTLEMENTS = 5     # Number of settlement clusters
MIN_SETTLE_SIZE = 5     # Minimum size of a settlement
MAX_SETTLE_SIZE = 10    # Maximum size of a settlement
FIRE_SPREAD_PROBS = [0.8, 0.05, 0.002]     # Probability that a fire will spread to a neigbouring tree, (index+1) in array corresponds to distance away from burning tree
MIN_BIOMASS = 1       # Minimum time a tree should burn for
MAX_BIOMASS = 8       # Maximum time a tree should burn for
FIREBREAK_WIDTH = 2     # Width of the fire break
WATERING_PROB = 0.4     # Probability that water puts out a cell on fire
STATION_RADIUS = 10
STATION_POWER = 5

EMPTY, TREE, FIRE, BURNT, SETTLE, SETTLE_FIRE, WET_TREE, WATER_STATION, WET_SETTLE, SETTLE_BURNT = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9   # Values corresponding to each state
COLORS = ['white', 'forestgreen', 'red', 'black', 'purple', 'red', 'aqua', 'darkblue', 'violet', 'gray']   # Color for each state


# Watering:
# Supress / reduce FIRE_SPREAD_PROBS in watered zone

# Firebreak:
# Remove trees in area

# Fuelbreak:
# Reduce biomass in area

# Controlled burns ???
