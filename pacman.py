WIDTH = 640
HEIGHT = 640
TITLE = 'Pac-Man'

# Create empty array to store the map from text file
world = []

def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line.strip():
                row.append(block)
            world.append(row)

load_level(1)
print(world)
