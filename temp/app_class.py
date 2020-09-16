import sys

import pygame
from temp.settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # To control frames per second
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = START
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.load()

    def run(self):
        while self.running:
            if self.state == START:
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == PLAYING:
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
        pygame.quit()
        sys.exit()

    ########################## HELP FUNC ############################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load("maze.png")
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY,
                             (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY,
                             (0, x * self.cell_height), (WIDTH, x * self.cell_height))

    ########################## START FUNC ############################

    def start_events(self):
        # Loop on list of all events that have happened
        # since the last time this is being called
        for event in pygame.event.get():
            # When use press ECS button to exit
            if event.type == pygame.QUIT:
                self.running = False
            # When user press SPACE to start the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = PLAYING

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(PUSH_SPACE_BAR, self.screen, [WIDTH // 2, HEIGHT // 2],
                       START_TEXT_SIZE, ORANGE, START_FONT, centered=True)

        self.draw_text(START_THE_GAME, self.screen, [WIDTH // 2, HEIGHT // 2 + 50],
                       START_TEXT_SIZE, ORANGE, START_FONT, centered=True)

        self.draw_text(EXIT_THE_GAME, self.screen, [WIDTH // 2, HEIGHT // 2 + 100],
                       START_TEXT_SIZE, BLUE, START_FONT, centered=True)

        self.draw_text(HIGH_SCORE, self.screen, [4, 4],
                       START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()

    ########################## PLAYING FUNC ############################

    def playing_events(self):
        # Loop on list of all events that have happened
        # since the last time this is being called
        for event in pygame.event.get():
            # When use press ECS button
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        pass

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_grid()
        self.draw_text(CURRENT_SCORE, self.screen, [60, 5], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text(HIGH_SCORE, self.screen, [WIDTH//2 + 60, 5], START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()
