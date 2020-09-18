import pygame
from settings import *
from player_class import *
from enemy_class import *

vec = pygame.math.Vector2


def draw_text(words, screen, pos, size, colour, font_name, centered=False):
    font = pygame.font.SysFont(font_name, size)
    text = font.render(words, False, colour)
    text_size = text.get_size()
    if centered:
        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)


class View:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.coins = []
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.e_pos = []
        self.p_pos = None
        self.walls = []
        self.coins = []
        self.enemies = []
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.load()

    # def load(self):
    #     self.background = pygame.image.load('maze.png')
    #     self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
    #
    #     # Opening walls file
    #     # Creating walls list with co-ords of walls
    #     # stored as  a vector
    #     with open("walls.txt", 'r') as file:
    #         for yidx, line in enumerate(file):
    #             for xidx, char in enumerate(line):
    #                 if char == "1":
    #                     self.walls.append(vec(xidx, yidx))
    #                 elif char == "C":
    #                     self.coins.append(vec(xidx, yidx))
    #                 elif char == "P":
    #                     self.p_pos = [xidx, yidx]
    #                 elif char in ["2", "3", "4", "5"]:
    #                     self.e_pos.append([xidx, yidx])
    #                 elif char == "B":
    #                     pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
    #                                                               self.cell_width, self.cell_height))
    #
    # def draw_grid(self):
    #     for x in range(WIDTH // self.cell_width):
    #         pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
    #                          (x * self.cell_width, HEIGHT))
    #     for x in range(HEIGHT // self.cell_height):
    #         pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
    #                          (WIDTH, x * self.cell_height))
    #
    # def draw_coins(self):
    #     for coin in self.coins:
    #         pygame.draw.circle(self.screen, (124, 123, 7),
    #                            (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
    #                             int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)
    #
    # def make_enemies(self):
    #     for idx, pos in enumerate(self.e_pos):
    #         self.enemies.append(Enemy(self, vec(pos), idx))
    #
    # def start_draw(self):
    #     self.screen.fill(BLACK)
    #     draw_text('PUSH SPACE BAR', self.screen, [
    #         WIDTH // 2, HEIGHT // 2 - 50], GENERAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
    #     draw_text('1 PLAYER ONLY', self.screen, [
    #         WIDTH // 2, HEIGHT // 2 + 50], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
    #     pygame.display.update()
    #
    # def playing_draw(self):
    #     self.screen.fill(BLACK)
    #     self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
    #     self.draw_coins()
    #     # self.draw_grid()
    #     draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
    #               self.screen, [60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
    #
    #     draw_text('HIGH SCORE: {}'.format(open("high_score.txt", "r").read()),
    #               self.screen, [WIDTH // 2 + 60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
    #     self.player.draw()
    #     for enemy in self.enemies:
    #         enemy.draw()
    #     pygame.display.update()
    #
    # def game_over_draw(self):
    #     self.screen.fill(BLACK)
    #     draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
    #     draw_text(AGAIN_TEXT, self.screen, [
    #         WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
    #     draw_text(QUIT_TEXT, self.screen, [
    #         WIDTH // 2, HEIGHT // 1.5], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
    #     pygame.display.update()
    #
    # def game_defeated_draw(self):
    #     draw_text('YOU WIN', self.screen, [
    #         WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
    #     draw_text(AGAIN_TEXT, self.screen, [
    #         WIDTH // 2, HEIGHT // 2 + 50], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
    #     draw_text(QUIT_TEXT, self.screen, [
    #         WIDTH // 2, HEIGHT // 2 + 100], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
    #     pygame.display.update()
