import pygame
from mvc_temp.settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, pos):
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self, walls, coins):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move(walls)
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            CELL_HEIGHT // 2) // CELL_HEIGHT + 1
        if self.on_coin(coins):
            self.eat_coin(coins)

    def draw(self, main_screen):
        pygame.draw.circle(main_screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                        int(self.pix_pos.y)), CELL_WIDTH // 2 - 2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(main_screen, PLAYER_COLOUR, (30 + 20 * x, HEIGHT - 15), 7)

    def on_coin(self, coins):
        if self.grid_pos in coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % CELL_WIDTH == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % CELL_HEIGHT == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self, coins):
        coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * CELL_WIDTH) + TOP_BOTTOM_BUFFER // 2 + CELL_WIDTH // 2,
                   (self.grid_pos[1] * CELL_HEIGHT) +
                   TOP_BOTTOM_BUFFER // 2 + CELL_HEIGHT // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % CELL_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % CELL_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self, walls):
        for wall in walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
