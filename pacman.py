# GAME CONSTANTS
WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE

TITLE = "Pac-Man"

# Add Pac-Man at the top left of the screen
pacman = Actor("pacman_o.png", anchor=("left", "top"))
pacman.x = pacman.y = 1 * BLOCK_SIZE

# Used to track direction in x and y
pacman.dx, pacman.dy = 0, 0

# Map char to image using dictionary
char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "r": "ghost1.png",
    "b": "ghost2.png"}

# Create empty array to store the map from text file
world = []


# Load the world depending on level file
def load_level(number):
    file = "level-%s.txt" % number

    # Start reading file process
    with open(file) as f:
        for line in f:
            row = []

            # Remove newline using string.strip()
            for block in line.strip():
                row.append(block)
            world.append(row)


# Draw the game on the screen
def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x * BLOCK_SIZE, y * BLOCK_SIZE))

    pacman.draw()


# Pac-Man movement
def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -1
    if key == keys.RIGHT:
        pacman.dx = 1
    if key == keys.UP:
        pacman.dy = -1
    if key == keys.DOWN:
        pacman.dy = 1


# Keep Pac-Man direction as key is released
def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


# Update Pac-Man position
def update():
    # To go in direction (dx, dy) check for no walls
    if '=' not in blocks_ahead_of_pacman(pacman.dx, 0):
        pacman.x += pacman.dx
    if '=' not in blocks_ahead_of_pacman(0, pacman.dy):
        pacman.y += pacman.dy


# Coll detection
def blocks_ahead_of_pacman(dx, dy):
    """Return a list of tiles at this position + (dx,dy)"""

    # Here's where we want to move to
    x = pacman.x + dx
    y = pacman.y + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix + 1])
    if ry:
        blocks.append(world[iy + 1][ix])
    if rx and ry:
        blocks.append(world[iy + 1][ix + 1])

    return blocks


load_level(1)
print(world)
