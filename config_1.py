SEED_VAL = 2    # Seed value for the random generator (repeatable results)
WIDTH, HEIGHT = 100, 100    # Size of the system
TREE_PROB = 0.6         # Density of the forest
NUM_SETTLEMENTS = 8     # Number of settlement clusters
MIN_SETTLE_SIZE = 5     # Minimum size of a settlement
MAX_SETTLE_SIZE = 10    # Maximum size of a settlement
FIRE_SPREAD_PROBS = [0.8, 0.05, 0.002]     # Probability that a fire will spread to a neigbouring tree, (index+1) in array corresponds to distance away from burning tree
MIN_BIOMASS = 1       # Minimum time a tree should burn for
MAX_BIOMASS = 8       # Maximum time a tree should burn for
FIREBREAK_WIDTH = 2     # Width of the fire break
STATION_RADIUS =7     # Radius that water station can reach
STATION_POWER = 3       # Number of trees that a water station can water each iteration

VALUES = [0,1,2,3,4,5,6,7,8,9]
EMPTY, TREE, SETTLE, WATER_STATION, FIRE, SETTLE_FIRE, BURNT, SETTLE_BURNT, WET_TREE, WET_SETTLE = VALUES
COLORS = ['white', 'forestgreen', 'purple', 'aqua', 'red', 'firebrick', 'black', 'saddlebrown', 'cornflowerblue', 'royalblue']

# Watering:
# Supress / reduce FIRE_SPREAD_PROBS in watered zone

# Firebreak:
# Remove trees in area

# Fuelbreak:
# Reduce biomass in area

# Controlled burns ???
