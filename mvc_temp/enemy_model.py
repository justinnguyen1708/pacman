import pygame
import random
from mvc_temp.settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, pos, number):
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(CELL_WIDTH // 2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self, player, walls):
        self.target = self.set_target(player)
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move(walls)

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            CELL_HEIGHT // 2) // CELL_HEIGHT + 1

    def draw(self, main_screen):
        pygame.draw.circle(main_screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self, player):
        if self.personality == "speedy" or self.personality == "slow":
            return player.grid_pos
        else:
            if player.grid_pos[0] > COLS // 2 and player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if player.grid_pos[0] > COLS // 2 and player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if player.grid_pos[0] < COLS // 2 and player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % CELL_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % CELL_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self, walls):
        if self.personality == "random":
            self.direction = self.get_random_direction(walls)
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target, walls)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target, walls)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target, walls)

    def get_path_direction(self, target, walls):
        next_cell = self.find_next_cell_in_path(target, walls)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target, walls):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
            int(target[0]), int(target[1])], walls)
        return path[1]

    def BFS(self, start, target, walls):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self, walls):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec((self.grid_pos.x * CELL_WIDTH) + TOP_BOTTOM_BUFFER // 2 + CELL_WIDTH // 2,
                   (self.grid_pos.y * CELL_HEIGHT) + TOP_BOTTOM_BUFFER // 2 + CELL_HEIGHT // 2)

    def set_colour(self):
        if self.number == 0:
            return GHOST_COLOUR_1
        if self.number == 1:
            return GHOST_COLOUR_2
        if self.number == 2:
            return GHOST_COLOUR_3
        if self.number == 3:
            return GHOST_COLOUR_4

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"
