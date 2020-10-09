import sys

from enemy_model import *
from player_model import *
from view import *

pygame.init()
vec = pygame.math.Vector2


class Controller:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load('maze.png')
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 0
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.player = None
        self.view = View()
        self.high_score = int(open(HIGH_SCORE, "r").read())

    # Get coins
    def get_coins(self):
        return self.coins

    # Get screen
    def get_screen(self):
        return self.screen

    # Get enemies
    def get_enemies(self):
        return self.enemies

    # Get player
    def get_player(self):
        return self.player

    # Get background
    def get_background(self):
        return self.background

    # Get walls
    def get_walls(self):
        return self.walls

    # Get high score
    def get_high_score(self):
        return self.high_score

    # Set high score
    def set_high_score(self, high_score):
        self.high_score = high_score

    def run(self):
        self.load()
        self.make_enemies()

        while self.running:
            if self.state == START_STATE:
                self.start_events()
                self.start_update()
                self.view.start_draw(self.get_screen())
            elif self.state == PLAYING_STATE:
                self.playing_events()
                self.playing_update()
                self.view.playing_draw(self.get_screen(), self.get_player(), self.get_enemies(),
                                       self.get_coins(), self.get_background(), self.get_high_score())
            elif self.state == GAME_OVER_STATE:
                self.game_over_events()
                self.game_over_update()
                self.view.game_over_draw(self.get_screen())
            elif self.state == GAME_DEFEATED_STATE:
                self.game_defeated_events()
                self.game_defeated_update()
                self.view.game_defeated_draw()
            else:
                self.running = False
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ############################ HELPER FUNCTIONS ##################################
    def update_high_score(self):
        if self.player.current_score > self.high_score:
            self.set_high_score(self.player.current_score)
            f = open(HIGH_SCORE, "w")
            f.write(str(self.player.current_score))
            f.close()

    def load(self):
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player = Player(vec([xidx, yidx]))
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * CELL_WIDTH, yidx * CELL_HEIGHT // ROWS,
                                                                  CELL_WIDTH, CELL_HEIGHT // ROWS))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(vec(pos), idx))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = PLAYING_STATE

    ########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = PLAYING_STATE

    def start_update(self):
        pass

    ########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        if len(self.coins) == 0:
            self.state = GAME_DEFEATED_STATE
        else:
            self.player.update(self.get_walls(), self.get_coins())
            for enemy in self.enemies:
                enemy.update(self.get_player(), self.get_walls())

            for enemy in self.enemies:
                if enemy.grid_pos == self.player.grid_pos:
                    self.remove_life()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = GAME_OVER_STATE
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    ########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def game_over_update(self):
        self.update_high_score()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    ########################### GAME DEFEATED FUNCTIONS ################################

    def game_defeated_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def game_defeated_update(self):
        self.update_high_score()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
